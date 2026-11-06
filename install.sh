#!/usr/bin/env bash
# AI Visibility Team: installs all 24 skills into ~/.claude/skills. Safe to run again.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SKILLS="${HOME}/.claude/skills"
mkdir -p "$SKILLS"

echo "→ ai-brand-test"
rm -rf "$SKILLS/ai-brand-test" && cp -R "$HERE/skills/ai-brand-test" "$SKILLS/"

echo "→ Humanizer (github.com/blader/humanizer)"
[ -d "$SKILLS/humanizer" ] || git clone --quiet --depth 1 https://github.com/blader/humanizer "$SKILLS/humanizer"

echo "→ Claude SEO (github.com/AgriciDaniel/claude-seo), using its own installer"
curl -fsSL https://raw.githubusercontent.com/AgriciDaniel/claude-seo/main/install.sh | bash

cat <<'EOF'

Done. Two last steps:
  1. Save your treg.to key:  mkdir -p ~/.config/treg && echo "YOUR_KEY" > ~/.config/treg/key
  2. In Claude Code, run:    /seo setup
Then ask Claude: "Does ChatGPT recommend my business? Run the AI brand test."
EOF
