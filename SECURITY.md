# Security Policy

This project executes system commands defined in `recipes.yaml`.
To use it safely:

- Review every command in recipes before running.
- Keep commands minimal; prefer package managers over raw scripts.
- Run inside a disposable VM or container if testing untrusted recipes.
- Limit `ALLOW_CMDS` in `agent.py` to only what you need.
- Consider read-only mounts when using Docker recipes.

Report issues via GitHub issues.
