# If You Are An AI Agent

Install or update `codex-ppt` into the user's Codex skills directory.

Prefer a native skill installation tool if the current environment provides one. Otherwise run:

```bash
set -euo pipefail

SKILLS_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
DEST="$SKILLS_ROOT/codex-ppt"

mkdir -p "$SKILLS_ROOT"

if [ -d "$DEST/.git" ]; then
  git -C "$DEST" pull --ff-only
else
  git clone https://github.com/Scott-Du/codex-ppt.git "$DEST"
fi

test -f "$DEST/SKILL.md"
test -f "$DEST/scripts/assemble_image_ppt.py"

git -C "$DEST" rev-parse --short HEAD
```

After installation, tell the user:

- whether the skill was installed or updated
- the install path
- the current commit
- whether they need to restart Codex or reload skills
