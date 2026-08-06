#!/usr/bin/env bash
# ASD Framework — Installer
# https://github.com/ibernabel/asd-framework
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/ibernabel/asd-framework/main/install.sh | bash
#   curl -fsSL ... | bash -s -- --domain software
#   curl -fsSL ... | bash -s -- --domain software --domain content
#   curl -fsSL ... | bash -s -- --domain all

set -euo pipefail

# ─── Config ─────────────────────────────────────────────────────────────────
AGENTS_DIR="${HOME}/.agents"
REPO_RAW="https://raw.githubusercontent.com/ibernabel/asd-framework/main"
ALL_DOMAINS=("software" "admin" "ai-agent" "content" "video")
SELECTED_DOMAINS=()
INSTALL_ALL=false

# ─── Colors ─────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

log()   { echo -e "${GREEN}✅ $*${NC}"; }
warn()  { echo -e "${YELLOW}⚠️  $*${NC}"; }
info()  { echo -e "${BLUE}ℹ️  $*${NC}"; }
error() { echo -e "${RED}❌ $*${NC}"; exit 1; }

# ─── Argument parsing ────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --domain)
      shift
      if [[ "$1" == "all" ]]; then
        INSTALL_ALL=true
      else
        SELECTED_DOMAINS+=("$1")
      fi
      ;;
    -h|--help)
      echo "Usage: install.sh [--domain <domain>] [--domain all]"
      echo "Domains: software, admin, ai-agent, content, video, all"
      exit 0
      ;;
  esac
  shift
done

# Default to all if nothing selected
if [[ ${#SELECTED_DOMAINS[@]} -eq 0 ]] && [[ "$INSTALL_ALL" == false ]]; then
  info "No domain specified — installing all domains."
  INSTALL_ALL=true
fi

if [[ "$INSTALL_ALL" == true ]]; then
  SELECTED_DOMAINS=("${ALL_DOMAINS[@]}")
fi

# ─── Domain → template file map ─────────────────────────────────────────────
declare -A TEMPLATE_MAP=(
  ["software"]="software-dev-agents.md"
  ["admin"]="business-admin-agents.md"
  ["ai-agent"]="ai-agents-agents.md"
  ["content"]="content-brand-agents.md"
  ["video"]="video-production-agents.md"
)

# ─── Setup ───────────────────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ASD Framework Installer"
echo "  github.com/ibernabel/asd-framework"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Create base directory structure
mkdir -p "${AGENTS_DIR}/templates"
mkdir -p "${AGENTS_DIR}/workflows"
log "Created ~/.agents/ structure"

# ─── Download domain templates ───────────────────────────────────────────────
info "Installing domains: ${SELECTED_DOMAINS[*]}"

for domain in "${SELECTED_DOMAINS[@]}"; do
  template="${TEMPLATE_MAP[$domain]:-}"
  if [[ -z "$template" ]]; then
    warn "Unknown domain '$domain' — skipping"
    continue
  fi

  curl -fsSL "${REPO_RAW}/templates/${template}" \
    -o "${AGENTS_DIR}/templates/${template}" \
    && log "Template installed: ${template}" \
    || warn "Failed to download template: ${template}"
done

# ─── Install CONVENTIONS template ────────────────────────────────────────────
if [[ " ${SELECTED_DOMAINS[*]} " =~ " software " ]]; then
  curl -fsSL "${REPO_RAW}/templates/CONVENTIONS-software.md" \
    -o "${AGENTS_DIR}/templates/CONVENTIONS-software.md" \
    && log "CONVENTIONS-software.md template installed" \
    || warn "Failed to download CONVENTIONS-software.md"
fi

# ─── Install workflows ───────────────────────────────────────────────────────
for wf in project-init repo-sync post-session-doc code-pipeline; do
  curl -fsSL "${REPO_RAW}/workflows/${wf}.md" \
    -o "${AGENTS_DIR}/workflows/${wf}.md" \
    && log "Workflow installed: ${wf}.md" \
    || warn "Failed to download workflow: ${wf}.md"
done

# ─── Install Uncle Bob Pipeline agents (software domain) ─────────────────────
if [[ " ${SELECTED_DOMAINS[*]} " =~ " software " ]]; then
  info "Installing Uncle Bob Pipeline agents..."
  mkdir -p "${AGENTS_DIR}/agents"

  PIPELINE_AGENTS=("orchestrator" "specifier" "coder" "refactorer" "architect" "qa" "pii-verifier")
  for agent in "${PIPELINE_AGENTS[@]}"; do
    mkdir -p "${AGENTS_DIR}/agents/${agent}"
    curl -fsSL "${REPO_RAW}/agents/${agent}/agent.md" \
      -o "${AGENTS_DIR}/agents/${agent}/agent.md" \
      && log "Agent installed: ${agent}" \
      || warn "Failed to download agent: ${agent}"
  done
fi

# ─── Post-installation ───────────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ ASD Framework installed!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
info "Next steps:"
echo "  1. Open any project in your AI agent IDE"
echo "  2. Run: /project-init"
echo "  3. Select your domain when prompted"
echo ""
info "Highly recommended — Matt Pocock's skills:"
echo "  https://github.com/mattpocock/skills"
echo "  Use the 'setup-matt-pocock-skills' skill to install them"
echo ""
info "Documentation:"
echo "  https://github.com/ibernabel/asd-framework"
echo ""
