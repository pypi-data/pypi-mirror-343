import shutil
from pathlib import Path

def init():
    print("[*] Initialisation du projet avec globalMem...")

    project_root = Path.cwd()
    vscode_dir = project_root / ".vscode"
    vscode_dir.mkdir(exist_ok=True)

    settings_file = vscode_dir / "settings.json"
    if not settings_file.exists():
        settings_file.write_text('''
{
  "python.analysis.stubPath": "./src/globalMem",
  "python.analysis.extraPaths": ["./src"],
  "python.analysis.useLibraryCodeForTypes": true
}
''')
        print("[+] .vscode/settings.json généré.")

    makefile = project_root / "Makefile"
    if not makefile.exists():
        makefile.write_text('''
.PHONY: setup build publish bump-patch bump-minor bump-major pyi clean

setup:
\tpython scripts/setup_dev_env.py

build:
\tpython -m build

publish:
\ttwine upload dist/*

bump-patch:
\tpython scripts/bump_version.py patch

bump-minor:
\tpython scripts/bump_version.py minor

bump-major:
\tpython scripts/bump_version.py major

pyi:
\tpython scripts/generate_pyi_from_globals.py src/globalMem/global_context.py

clean:
\trm -rf build dist *.egg-info
\tfind . -name "__pycache__" -exec rm -r {} +
''')
        print("[+] Makefile généré.")

    print("[✓] Projet configuré avec globalMem.")
