# autopm/tracker.py
import builtins
import sys
from importlib.metadata import distribution, PackageNotFoundError
import subprocess
import os

# Save the original import function
original_import = builtins.__import__
# Keep track of which top-level packages we've seen
seen = set()
# Prevent our hook from re-entering itself
_in_hook = False

def try_auto_install(package_name):
    """
    Attempt to install a package using pip if it's not already available.
    """
    print(f"[autopm tracker] Attempting to auto-install: {package_name}")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    except Exception as e:
        print(f"[autopm tracker] Failed to auto-install {package_name}: {e}")


def custom_import(name, globals=None, locals=None, fromlist=(), level=0):
    global _in_hook
    if _in_hook or name.startswith('importlib'):
        return original_import(name, globals, locals, fromlist, level)

    top_level = name.split('.')[0]
    _in_hook = True
    try:
        if top_level not in sys.builtin_module_names and top_level not in seen:
            try:
                distribution(top_level)
            except PackageNotFoundError:
                try_auto_install(top_level)

        module = original_import(name, globals, locals, fromlist, level)

        # record requirement (but avoid duplicates)
        if top_level not in seen and top_level not in sys.builtin_module_names:
            seen.add(top_level)
            try:
                dist = distribution(top_level)
                version = dist.version
                req_line = f"{dist.metadata['Name']}=={version}\n"
                existing = []
                if os.path.exists("requirements.txt"):
                    with open("requirements.txt", "r") as f:
                        existing = f.readlines()
                if req_line not in existing:
                    with open("requirements.txt", "a") as f:
                        f.write(req_line)
            except (PackageNotFoundError, ValueError):
                pass
            except Exception:
                pass

        return module
    finally:
        _in_hook = False


def install_requirements_if_present():
    """
    Installs packages listed in requirements.txt using pip.
    If version conflicts exist, it attempts to resolve them.
    """
    if os.path.exists("requirements.txt"):
        print("[autopm tracker] Installing requirements...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install",
                "--upgrade", "--upgrade-strategy", "eager", "-r", "requirements.txt"
            ])
            print("[autopm tracker] Requirements installed successfully.")
        except subprocess.CalledProcessError:
            print("[autopm tracker] Failed to install requirements.")



def install_import_hook():
    print("[autopm tracker] Hooking into __import__")
    install_requirements_if_present()
    builtins.__import__ = custom_import
