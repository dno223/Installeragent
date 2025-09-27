# Contributing

1. Fork the repo and create a branch.
2. Keep recipes small and auditable.
3. Prefer OS package managers (`brew`, `apt`, `winget`) over cURL | bash.
4. Update `README.md` if you add a notable recipe.
5. Run CI locally:
   ```bash
   python -m py_compile agent.py
   python - <<'PY'
import yaml, sys
print("Loading recipes.yaml ...")
yaml.safe_load(open("recipes.yaml"))
print("OK")
PY
   ```
