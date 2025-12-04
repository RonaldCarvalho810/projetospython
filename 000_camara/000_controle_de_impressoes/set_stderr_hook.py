# set_stderr_hook.py
import sys, os

# Garantir sys.stderr
try:
    if sys.stderr is None or not hasattr(sys.stderr, "write"):
        sys.stderr = open(os.devnull, "w", encoding="utf-8", errors="ignore")
except Exception:
    pass

# Garantir sys.stdout
try:
    if sys.stdout is None or not hasattr(sys.stdout, "write"):
        sys.stdout = open(os.devnull, "w", encoding="utf-8", errors="ignore")
except Exception:
    pass
