# ModBridge.py
# Generic Windows EXE launcher configurable using ModBridge.ini (next to this exe).
# Features:
# - Can replace any game.exe and launch any other .exe instead
# - Profiles (select via -p Name, default is [Mod])
# - Target .exe path, working dir, extra args from INI
# - Relative paths (relative to this launcher) and %ENVVAR% expansion
# - Optional pass-through of command-line args
# - Waits for child so Steam overlay works every time
# - Optional environment overrides from [Env] section

import os
import sys
import shlex
import subprocess
from pathlib import Path
import configparser

def _msgbox(title, text):
	try:
		import ctypes
		ctypes.windll.user32.MessageBoxW(0, str(text), str(title), 0x10)  # MB_ICONERROR
	except Exception:
		print(f"{title}: {text}")

def _bool(s, default=False):
	if s is None:
		return default
	return str(s).strip().lower() in {"1", "true", "yes", "on"}

def _resolve_path(base: Path, p: str) -> Path:
	# Expand %ENVVARS% and ~ and make absolute relative to base, strip quotations
	exp = os.path.expandvars(os.path.expanduser(p.strip().strip('"').strip("'")))
	pp = Path(exp)
	if not pp.is_absolute():
		pp = base / pp
	return pp.resolve()

def _parse_profile_arg(argv):
	# Accepts "-p Name" launch argument to select custom profile
	name = None
	for i, a in enumerate(argv):
		if a == "-p" and i + 1 < len(argv):
			return argv[i + 1].strip()
	return None

def main():
	here = Path(sys.argv[0]).resolve().parent
	ini_path = here / "ModBridge.ini"

	if not ini_path.exists():
		_msgbox("ModBridge Error", f"Missing ModBridge.ini next to:\n{sys.argv[0]}")
		sys.exit(1)

	cfg = configparser.RawConfigParser()
	try:
		with ini_path.open("r", encoding="utf-8") as f:
			cfg.read_file(f)
	except Exception as e:
		_msgbox("ModBridge Error", f"Failed to read INI:\n{ini_path}\n\n{e}")
		sys.exit(1)

	# Pick profile
	profile = _parse_profile_arg(sys.argv[1:]) or "Mod"
	if profile not in cfg.sections():
		# If no [Mod] but there is only one profile use that
		sections = cfg.sections()
		if profile == "Mod" and len(sections) == 1:
			profile = sections[0]
		else:
			_msgbox("ModBridge Error", f"Profile [{profile}] not found in {ini_path}")
			sys.exit(1)

	section = cfg[profile]

	# Read settings
	target_str = section.get("Target", fallback=None)
	if not target_str:
		_msgbox("ModBridge Error", f"[{profile}] must define Target=path\\to\\mod.exe")
		sys.exit(1)

	workdir_str = section.get("WorkDir", fallback=None)
	args_str = section.get("Args", fallback="")  # extra args from INI
	inherit_args = _bool(section.get("InheritArgs", fallback="true"), default=True)
	wait_child = _bool(section.get("Wait", fallback="true"), default=True)

	# Resolve paths
	target_exe = _resolve_path(here, target_str)
	working_dir = _resolve_path(here, workdir_str) if workdir_str else target_exe.parent

	if not target_exe.exists():
		_msgbox("ModBridge Error", f"Target not found:\n{target_exe}")
		sys.exit(1)
	
	if not working_dir.exists():
		_msgbox("ModBridge Error", f"WorkDir not found:\n{working_dir}")
		sys.exit(1)

	# Build argument vector
	cmd = [str(target_exe)]
	if args_str.strip():
		# Windows-aware splitting
		cmd.extend(shlex.split(args_str, posix=False))
	if inherit_args:
		# Pass through any args given to ModBridge
		passthrough = []
		skip_next = False
		for i, a in enumerate(sys.argv[1:]):
			if skip_next:
				skip_next = False
				continue
			if a == "-p":
				if i + 1 < len(sys.argv[1:]):
					skip_next = True
				continue
			passthrough.append(a)
		cmd.extend(passthrough)

	# Advanced environment overrides from [Env]
	env = os.environ.copy()
	if "Env" in cfg:
		for k, v in cfg["Env"].items():
			env[k] = os.path.expandvars(os.path.expanduser(v))

	try:
		if wait_child:
			# Keep parent process running to make sure Steam overlay works with launchers/slow exe
			proc = subprocess.Popen(cmd, cwd=str(working_dir), close_fds=False, env=env)
			rc = proc.wait()
			sys.exit(rc)
		else:
			subprocess.Popen(cmd, cwd=str(working_dir), close_fds=False, env=env)
			sys.exit(0)
	except Exception as e:
		_msgbox("ModBridge failed to start", e)
		sys.exit(1)

if __name__ == "__main__":
	main()
