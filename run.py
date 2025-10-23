#!/usr/bin/env python3
"""
run.py - Primary launcher (entry-point) for MAK LIMAH BIADAB.

Purpose:
- This script is intended to be the *first* script you run.
- It locates the real tool script (prefer `src/mak-limah.py`, fallback to `mak-limah.py`),
  prepares a minimal environment, optionally installs dependencies, and executes the tool
  as a separate process so the tool runs in its own working directory (preserving relative imports).

Usage:
    # Basic run (will find src/mak-limah.py or mak-limah.py)
    python3 run.py --target https://example.com

    # Install dependencies first (rich, requests)
    python3 run.py --install-deps --target https://example.com

    # Pass-through arguments to the tool (everything after --)
    python3 run.py --target https://example.com -- --mode full --export-ci

    # Use virtualenv creation (optional)
    python3 run.py --create-venv venv --install-deps --target https://example.com

Notes:
- You must have permission to scan the target. Unauthorized scanning is illegal.
- This launcher executes the tool as a subprocess to keep the environment isolated.
"""

import sys
import shutil
import subprocess
import argparse
from pathlib import Path

DEFAULT_PACKAGES = ["rich", "requests"]

def find_tool_path():
    """Look for src/mak-limah.py first, then mak-limah.py in cwd."""
    candidates = [Path("src") / "mak-limah.py", Path("mak-limah.py")]
    for p in candidates:
        if p.exists():
            return p.resolve()
    return None

def install_packages(packages, python_exe=None):
    py = python_exe or sys.executable
    cmd = [py, "-m", "pip", "install", *packages]
    print("Installing packages:", " ".join(packages))
    return subprocess.call(cmd) == 0

def create_venv(venv_path: Path):
    if venv_path.exists():
        print(f"Virtualenv {venv_path} already exists. Skipping creation.")
        return True
    print(f"Creating virtualenv at {venv_path} ...")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_path)])
        print("Virtualenv created.")
        return True
    except subprocess.CalledProcessError as e:
        print("Failed to create virtualenv:", e)
        return False

def main():
    parser = argparse.ArgumentParser(description="Primary launcher for MAK LIMAH BIADAB")
    parser.add_argument("--install-deps", action="store_true", help="Install required Python packages (rich, requests).")
    parser.add_argument("--create-venv", nargs='?', const="venv", help="Create a virtualenv at the given path (default: venv).")
    parser.add_argument("--target", help="Target URL (optional pass-through to tool).")
    parser.add_argument("pass_args", nargs=argparse.REMAINDER, help="Arguments to pass to the tool (prefix with --).")
    args = parser.parse_args()

    tool_path = find_tool_path()
    if not tool_path:
        print("Error: Could not find src/mak-limah.py or mak-limah.py. Please place the tool file accordingly.")
        sys.exit(2)

    # Optionally create a venv and adjust python executable
    python_exe = sys.executable
    if args.create_venv:
        venv_dir = Path(args.create_venv)
        created = create_venv(venv_dir)
        if not created:
            print("Exiting due to venv creation failure.")
            sys.exit(3)
        # Use the venv's python
        if sys.platform == "win32":
            python_exe = venv_dir / "Scripts" / "python.exe"
        else:
            python_exe = venv_dir / "bin" / "python"

    # Install deps if requested (into chosen python executable)
    if args.install_deps:
        ok = install_packages(DEFAULT_PACKAGES, python_exe=str(python_exe))
        if not ok:
            print("Dependency installation failed. You may install manually: pip install rich requests")
            # Continue anyway; the tool may still run if deps are present.

    # Build command to execute the tool as a separate process
    cmd = [str(python_exe), str(tool_path)]
    # If user provided a --target on this launcher and did not include it in pass_args, add it
    if args.target and "--target" not in " ".join(args.pass_args):
        cmd += ["--target", args.target]
    # Append pass-through arguments (if any)
    if args.pass_args:
        # argparse.REMAINDER includes the leading '--' if provided; strip it
        rem = list(args.pass_args)
        if rem and rem[0] == "--":
            rem = rem[1:]
        cmd += rem

    print("Launching tool:", " ".join(cmd))
    # Use the tool's parent directory as working directory so relative files (like outputs/) are created there
    workdir = tool_path.parent
    try:
        rc = subprocess.call(cmd, cwd=str(workdir))
        print(f"Tool exited with return code: {rc}")
        sys.exit(rc)
    except KeyboardInterrupt:
        print("Interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print("Failed to launch tool:", e)
        sys.exit(4)

if __name__ == "__main__":
    main()
