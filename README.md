# Installer Agent (Local App Installer with Recipes)

A tiny, auditable **local installer agent** that runs whitelisted commands to install apps on **macOS, Linux/WSL, and Windows**. It uses a simple `recipes.yaml` to describe installs. Includes working recipes for **OpenGRC** (native & Docker) and an example for **nginx**.

## Why this exists
- **Repeatable installs** you can version-control
- **Auditable**: prints every command it runs
- **Safe**: allowlist of commands + sandboxed working directory

---

## Quickstart (macOS / Linux / WSL)

```bash
# 1) Clone & enter
git clone <your-fork-url>.git installer-agent && cd installer-agent

# 2) Python deps (venv recommended)
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3) Run a recipe (OpenGRC native)
python agent.py opengrc --yes

# Or: Docker-based install
python agent.py opengrc_docker --yes
```

> macOS requires Homebrew. Linux/WSL recipes use `apt`. For Windows-native, use `winget` recipes (OpenGRC is recommended on WSL/Docker).

---

## How it works
- `python agent.py <recipe-name> [--yes]`
- Agent detects OS, loads `recipes.yaml`, and executes **only** commands in `ALLOW_CMDS` (see `agent.py`) inside the repo folder.
- Each step can set `cwd:` and an OS filter via `when:`.

### Recipe structure
```yaml
appname:
  os: ["mac","linux","wsl","windows"]
  steps:
    - run: <command>
      cwd: <dir>          # optional (defaults to ".")
      when: <os-string>   # optional ("mac"|"linux"|"wsl"|"windows")
  post_install_notes: |
    Tips printed at the end
```

### Included recipes
- **`opengrc`** – native install with all prerequisites.
- **`opengrc_docker`** – build & run via Docker Compose.
- **`nginx`** – small example for OS package managers.

---

## Security Model
- **Allowlist**: only commands listed in `ALLOW_CMDS` run.
- **Sandbox**: commands must run inside the repo folder or its children.
- **Visibility**: every command is printed before execution.

⚠️ You own the commands in `recipes.yaml`. Keep them minimal and trustworthy.

## Add your own app
1. Append a new block in `recipes.yaml`.
2. If a command is blocked, add its executable name to `ALLOW_CMDS` in `agent.py`.
3. Test:
   ```bash
   python agent.py <your-recipe> --yes
   ```

---

## Troubleshooting
- **Missing PHP intl** on macOS for OpenGRC:
  ```bash
  brew install php-intl
  ```
- **Docker not installed** for `opengrc_docker`: install Docker Desktop (mac/Win) or docker engine + compose on Linux.
- **Command not allowed**: add the executable to `ALLOW_CMDS` in `agent.py`.

---

## License
MIT
