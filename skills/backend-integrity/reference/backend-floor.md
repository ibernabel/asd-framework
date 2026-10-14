# Backend Floor: The 6 Non-Negotiable Architectural Rules

This reference document defines the quality floor for all backend services, endpoints, models, workers, and database operations. When writing backend code, agents must treat these rules as strict constraints.

---

## 1. Zero Mass-Assignment (Schema-First Input Validation)

**Rule:** Never pass raw HTTP payloads directly to an ORM, active record, or database query. All incoming data must be parsed, validated, and typed through an explicit schema.

### ❌ Refuse (Dangerous AI Default):
```python
# Python / Django / FastAPI
@app.post("/users")
def create_user(data: dict = Body(...)):
    user = User.objects.create(**data) # Security Risk: Mass assignment (e.g. is_superuser=True)
    return user
```
```typescript
// TypeScript / Express / Next.js
export async function POST(req: Request) {
  const body = await req.json();
  const user = await prisma.user.create({ data: body }); // Dangerous: Unvalidated fields
  return NextResponse.json(user);
}
```

### ✅ Require (Certified Pattern):
```python
# Pydantic schema validation
class CreateUserSchema(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(payload: CreateUserSchema):
    user = UserService.register(payload.model_dump())
    return user
```
```typescript
// Zod schema validation
const CreateUserSchema = z.object({
  name: z.string().min(2).max(100),
  email: z.string().email(),
});

export async function POST(req: Request) {
  const parsed = CreateUserSchema.parse(await req.json());
  const user = await UserService.register(parsed);
  return NextResponse.json(user, { status: 201 });
}
```

---

## 2. Transactional Atomicity (Multi-Mutation Integrity)

**Rule:** Any operation that updates or inserts across more than one table, document collection, or aggregate boundary MUST be enclosed within an atomic transaction. Partial writes that leave databases in inconsistent states are considered critical bugs.

### ❌ Refuse:
```python
# Failure halfway leaves an invoice with no line items or a broken balance
invoice = Invoice.objects.create(customer_id=customer_id)
for item in items:
    LineItem.objects.create(invoice=invoice, **item)
Customer.objects.filter(id=customer_id).update(balance=F('balance') - invoice.total)
```

### ✅ Require:
```python
from django.db import transaction

with transaction.atomic():
    invoice = Invoice.objects.create(customer_id=customer_id)
    LineItem.objects.bulk_create([LineItem(invoice=invoice, **item) for item in items])
    Customer.objects.filter(id=customer_id).update(balance=F('balance') - invoice.total)
```
```typescript
await prisma.$transaction(async (tx) => {
  const invoice = await tx.invoice.create({ data: invoiceData });
  await tx.lineItem.createMany({ data: items.map(i => ({ ...i, invoiceId: invoice.id })) });
  await tx.customer.update({ where: { id: customerId }, data: { balance: { decrement: total } } });
});
```

---

## 3. Strict I/O Resilience & Bounded Timeouts

**Rule:** Every outbound network call (`requests`, `httpx`, `fetch`, `axios`, gRPC, external queue, webhook) MUST declare an explicit timeout (default $\le 10\text{s}$) and include exponential backoff retries for transient network errors. Bare network calls without timeouts can permanently exhaust server worker threads.

### ❌ Refuse:
```python
response = requests.get("https://third-party.api/data") # No timeout! Blocks worker indefinitely on network hang
```
```typescript
const res = await fetch("https://third-party.api/data"); // No AbortSignal or timeout
```

### ✅ Require:
```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential_jitter, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=1, max=10),
    retry=retry_if_exception_type(httpx.NetworkError),
)
def fetch_external_quote(symbol: str) -> dict:
    with httpx.Client(timeout=5.0) as client: # Explicit 5s timeout
        response = client.get(f"https://quote.api/v1/{symbol}")
        response.raise_for_status()
        return response.json()
```
```typescript
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 5000); // 5s timeout
try {
  const res = await fetch("https://third-party.api/data", { signal: controller.signal });
} finally {
  clearTimeout(timeoutId);
}
```

---

## 4. Zero N+1 Queries & Mandatory Pagination

**Rule:**
1. Endpoints returning collections MUST enforce pagination (cursor-based or limit/offset). Returning unbounded result sets (`SELECT * FROM table`) causes memory exhaustion as datasets grow.
2. ORM queries inside loops MUST use eager loading (`select_related`, `prefetch_related`, `include`).

### ❌ Refuse:
```python
# N+1 query problem
orders = Order.objects.all() # No limit!
for order in orders:
    print(order.customer.name) # 1 query for orders + N queries for each customer
```

### ✅ Require:
```python
# Eager loading + pagination
orders = Order.objects.select_related("customer").order_by("-created_at")[:limit]
```

---

## 5. Layer Isolation (Clean / Hexagonal Architecture)

**Rule:**
- **Controllers / Route Handlers:** Only handle HTTP request validation, call application services, and return HTTP responses.
- **Application Services / Use Cases:** Orchestrate domain logic, transactions, and calls to external ports.
- **Domain Layer:** Pure business entities and rules, independent of HTTP, frameworks, or databases.
- Prohibited: Writing direct SQL queries or multi-step domain logic inside HTTP route handlers.

---

## 6. Semantic Error Hierarchy

**Rule:** Never suppress exceptions with empty `except:` or `catch (e) {}`. All application errors must map to structured error payloads with standard HTTP status codes:

- `400 Bad Request`: Malformed syntax.
- `401 Unauthorized`: Missing or invalid authentication token.
- `403 Forbidden`: Authenticated user lacks permission (RBAC).
- `404 Not Found`: Resource does not exist.
- `409 Conflict`: Business rule violation (e.g. duplicate unique key).
- `422 Unprocessable Entity`: Semantic/schema validation failure.
- `500 Internal Server Error`: Unhandled server exception (logged with stack trace and correlation ID).

### Standard Error Response Shape:
```json
{
  "error": {
    "code": "INSUFFICIENT_FUNDS",
    "message": "Account balance is insufficient for requested withdrawal",
    "details": {
      "requested": 500.0,
      "available": 120.5
    }
  }
}
```
