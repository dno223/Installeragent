import os, sys, platform, subprocess, shlex, yaml
from pathlib import Path
from rich import print
from rich.prompt import Confirm

# --- Config ---
SANDBOX = Path.cwd()  # restrict execution to this folder/subfolders
ALLOW_CMDS = {
    # package managers / basics
    "brew", "apt", "winget", "sudo",
    # common tools
    "git", "bash", "php", "composer", "node", "npm", "sqlite3",
    "ls", "pwd",
    # docker (needed for *docker recipes)
    "docker"
}

def detect_os():
    sysname = platform.system().lower()
    # macOS is 'Darwin'
    if "windows" in sysname:
        # WSL often shows as 'Linux' but has 'Microsoft' in release
        if "microsoft" in platform.release().lower():
            return "wsl"
        return "windows"
    if "darwin" in sysname:
        return "mac"
    return "linux"

def _ensure_in_sandbox(cwd_path: Path):
    # allow SANDBOX itself or any child of SANDBOX
    base = SANDBOX.resolve()
    target = cwd_path.resolve()
    if not (target == base or base in target.parents):
        raise RuntimeError("CWD outside sandbox.")

def safe_run(cmd, cwd=None):
    exe = shlex.split(cmd)[0]
    _ensure_in_sandbox(Path(cwd) if cwd else SANDBOX)
    if exe not in ALLOW_CMDS:
        raise RuntimeError(f"Command not allowed: {exe}")
    run_cwd = cwd or "."
    print(f"[bold]$ {cmd}[/bold]  (cwd={Path(run_cwd).resolve()})")
    subprocess.run(cmd, cwd=run_cwd, shell=True, check=True)

def run_recipe(name, recipes, target_os):
    if name not in recipes:
        raise SystemExit(f"Unknown recipe: {name}")
    r = recipes[name]
    if target_os not in r.get("os", []):
        raise SystemExit(f"Recipe {name} isn’t marked for OS {target_os}")
    print(f"[cyan]Running recipe:[/cyan] {name}  [dim]for {target_os}[/dim]")
    for s in r.get("steps", []):
        when = s.get("when")
        if when and when != target_os:
            continue
        safe_run(s["run"], cwd=s.get("cwd", "."))
    notes = r.get("post_install_notes")
    if notes:
        print(f"\n[green]Post-install notes:[/green]\n{notes}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python agent.py <recipe-name> [--yes]")
        sys.exit(1)

    target = sys.argv[1].lower()
    auto_yes = "--yes" in sys.argv
    os_name = detect_os()

    with open("recipes.yaml", "r", encoding="utf-8") as f:
        recipes = yaml.safe_load(f) or {}

    if target in recipes:
        print(f"[bold]About to run recipe:[/bold] {target} on {os_name}")
        if not auto_yes and not Confirm.ask("Proceed?"):
            sys.exit(0)
        run_recipe(target, recipes, os_name)
        return

    print(f"No recipe named '{target}'. Add it to recipes.yaml.")

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print(f"[red]Command failed:[/red] {e}")
        sys.exit(e.returncode)
    except Exception as e:
        print(f"[red]Error:[/red] {e}")
        sys.exit(1)
