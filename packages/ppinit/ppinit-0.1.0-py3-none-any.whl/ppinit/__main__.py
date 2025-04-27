import os
import sys
import toml
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Literal, Any
from argparse import ArgumentParser


ASSETS_DIR = Path(__file__).parent / "assets"
LICENSES_DIR = ASSETS_DIR / "licenses"


def install_deps(deps: str, pip_path: str | Path = "pip") -> None:
    if not deps:
        return
    print("📦 Installing dependencies...")
    subprocess.run([pip_path, "install"] + deps.split())


def create_venv(venv_path: str | Path, deps: str) -> str:
    subprocess.run([sys.executable, "-m", "venv", str(venv_path)])
    print(f"🐍 venv created at {venv_path}")
    
    if deps:
        install_deps(deps, os.path.join(venv_path, "Scripts" if os.name == "nt" else "bin", "pip"))

    venv_activate_cmd = (
        f"source {str(venv_path)}/bin/activate"
        if os.name != "nt"
        else f"{str(venv_path)}\\Scripts\\activate"
    )
    return venv_activate_cmd


def create_license(
    project_path: str | Path,
    license_type: Literal["MIT", "Apache-2.0", "AGPL-3.0", "GPL-3.0"],
    author: str = "Your Name"
) -> None:
    license_path = LICENSES_DIR / f"{license_type}.txt"
    if not license_path.exists():
        print(f"⚠️ License template for {license_type} not found.")
        return
    
    # Read, replace placeholders, and write to LICENSE
    content = license_path.read_text().format_map({"year": str(datetime.now().year), "author": author})
    (Path(project_path) / "LICENSE").write_text(content)

    print(f"📄 {license_type} LICENSE added.")


def create_toml_file(data: dict[str, Any], filepath: str | Path) -> None:
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(toml.dumps(data), encoding="utf-8")
    print(f"📝 TOML file created at {str(filepath)}")


def init_git(project_path: str | Path) -> None:
    print("🌱 ", end="", flush=True)
    subprocess.run(["git", "init"], cwd=project_path)


def init_project(
    name: str,
    version: str,
    desc: str,
    req_py: str,
    author: str,
    email: str,
    license: Literal["MIT", "Apache-2.0", "AGPL-3.0", "GPL-3.0"] | None,
    deps: str,
    use_venv: bool,
    use_git: bool,
    include_toml: bool,
    include_readme: bool
):
    project_path = Path(name)
    project_path.mkdir(exist_ok=True)

    # === Create virtual environment ===
    if use_venv:
        venv_activate_cmd = create_venv(project_path / "venv", deps)
    elif deps:
        install_deps(deps)

    # === Create the folders ===
    for folder in ["src"]:
        (project_path / folder).mkdir(exist_ok=True)
        (project_path / folder / "__init__.py").write_text("")

    # === Create the files ===
    shutil.copy(ASSETS_DIR / "main_file_content.txt", project_path / "src" / "main.py")
    shutil.copy(ASSETS_DIR / "gitignore_content.txt", project_path / ".gitignore")
    (project_path / "requirements.txt").write_text(deps.replace(" ", "\n"))

    if include_toml:
        data = {
            "project": {
                "name": name,
                "version": version,
                "description": desc,
                "requires-python": f">={req_py}",
                "authors": [{"name": name, "email": email}],
                "dependencies": deps.split(),
            },
        }
        if include_readme:
            data["project"]["readme"] = "README.md"
        if license:
            data["project"]["license"] = license
            data["project"]["license-files"] = ["LICEN[CS]E*"]
        if use_git:
            data["project"]["urls"] = {"Homepage": ""}


        create_toml_file(data, project_path / "pyproject.toml")

    if license:
        create_license(project_path, license, author)

    if include_readme:
        (project_path / "README.md").write_text(f"# {name}\n\n{desc or "Project description goes here."}\n")
        print(f"📄 README.md added.")

    # === Initialize git ===
    if use_git:
        init_git(project_path)

    print(f"✅ Project '{name}' is ready!")
    if use_venv:
        print(f"👉 To activate your virtual environment: {venv_activate_cmd}")


def main():
    parser = ArgumentParser(description="⚡ Python Project Initializer")

    parser.add_argument("name", help="Project name")
    parser.add_argument("--version", help="Project version", default="0.1.0")
    parser.add_argument("--desc", help="Project description", default="")
    parser.add_argument("--req-py", help="Requires python", default="3.10")
    parser.add_argument("--author", help="Author name", default="")
    parser.add_argument("--email", help="Author email", default="")
    parser.add_argument("--license", choices=["MIT", "Apache-2.0", "AGPL-3.0", "GPL-3.0"], help="Add a license file")
    parser.add_argument("--deps", help="Space-separated dependencies", default="")
    parser.add_argument("--venv", action="store_true", help="Create virtual environment")
    parser.add_argument("--git", action="store_true", help="Initialize Git repository")
    parser.add_argument("--no-toml", action="store_true", help="Skip creating myproject.toml")
    parser.add_argument("--no-readme", action="store_true", help="Skip creating README.md")

    args = parser.parse_args()

    init_project(
        name=args.name.strip(),
        version=args.version.strip(),
        desc=args.desc.strip(),
        req_py=args.req_py.strip(),
        author=args.author.strip(),
        email=args.email.strip(),
        license=args.license.strip(),
        deps=args.deps.strip(),
        use_venv=args.venv,
        use_git=args.git,
        include_toml=not args.no_toml,
        include_readme=not args.no_readme,
    )


if __name__ == "__main__":
    main()
