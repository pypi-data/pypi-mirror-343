"""Command-line interface for proj2md package."""

import datetime
import fnmatch
import os
import re
import subprocess
import unicodedata
from pathlib import Path
from typing import Literal

import click

try:
    import tomllib
except ModuleNotFoundError:
    try:
        import tomli as tomllib  # type: ignore
    except ModuleNotFoundError:
        tomllib = None  # type: ignore[assignment]


def parse_pyproject(input_dir: str) -> dict:
    """Parse pyproject.toml file to extract metadata.

    Args:
        input_dir (str): Path to the project directory.

    Returns:
        dict: Parsed data from pyproject.toml.
    """
    toml_path = os.path.join(input_dir, "pyproject.toml")
    if not os.path.isfile(toml_path) or tomllib is None:
        return {}
    try:
        with open(toml_path, "rb") as f:
            return tomllib.load(f)
    except Exception:
        return {}


def get_metadata(input_dir: str) -> dict:  # noqa: PLR0912, PLR0914
    """Extract metadata from pyproject.toml or git config.

    Args:
        input_dir (str): Path to the project directory.

    Returns:
        dict: Metadata including name, version, author, and dependencies.
    """
    data = parse_pyproject(input_dir)
    name = None
    version = None
    authors = []
    dependencies = []
    project = data.get("project")
    if project:
        name = project.get("name")
        version = project.get("version")
        deps = project.get("dependencies", [])
        if isinstance(deps, list):
            for dep in deps:
                if isinstance(dep, str):
                    pkg = dep.split()[0]
                    # Strip version specifiers (e.g. >=, ==, ~=)
                    name_only = re.split(r"[<>=!~]", pkg, 1)[0]
                    dependencies.append(name_only)
        authors_meta = project.get("authors", [])
        if isinstance(authors_meta, list):
            for a in authors_meta:
                if isinstance(a, dict):
                    n = a.get("name")
                    if n:
                        authors.append(n)
                elif isinstance(a, str):
                    authors.append(a.split("<")[0].strip())
    else:
        tool = data.get("tool", {})
        poetry = tool.get("poetry", {})
        if poetry:
            name = poetry.get("name")
            version = poetry.get("version")
            deps = poetry.get("dependencies", {})
            if isinstance(deps, dict):
                dependencies.extend(pkg for pkg in deps if pkg.lower() != "python")
            auths = poetry.get("authors", [])
            if isinstance(auths, list):
                authors.extend(a.split("<")[0].strip() for a in auths if isinstance(a, str))
    if not name:
        name = os.path.basename(os.path.abspath(input_dir))
    if not version:
        version = ""
    if not authors:
        try:
            result = subprocess.run(  # noqa: S603
                ["git", "config", "--get", "user.name"],  # noqa: S607
                cwd=input_dir,
                capture_output=True,
                text=True,
                check=False,
            )
            git_name = result.stdout.strip()
            if git_name:
                authors = [git_name]
        except Exception:  # noqa: S110
            pass
    author = ", ".join(authors) if authors else ""
    return {"name": name, "version": version, "author": author, "dependencies": dependencies}


def generate_tree(root: str, exclude_patterns: list[str] | None = None) -> str:
    """Generate a tree-like structure of the project directory.

    Args:
        root (str): Path to the project directory.
        exclude_patterns (list[str] | None): List of patterns to exclude from the tree.

    Returns:
        str: Tree-like structure of the project directory.
    """
    lines = []

    def inner(dir_path: str, prefix: str = "") -> None:
        """Recursively build the tree structure.

        Args:
            dir_path (str): Current directory path.
            prefix (str): Prefix for the current level of the tree.
        """
        try:
            # list entries, ignoring hidden, generated, and default-excluded files/dirs
            entries = sorted(
                e
                for e in os.listdir(dir_path)
                if not e.startswith(".")
                and not e.startswith("generated_")
                and not e.endswith(".lock")
                and not e.endswith(".egg-info")
                and e != "__pycache__"
            )
        except OSError:
            return
        # filter entries by exclude patterns
        filtered = []
        for name in entries:
            rel = os.path.relpath(os.path.join(dir_path, name), root)
            if exclude_patterns and any(fnmatch.fnmatch(rel, pat) for pat in exclude_patterns):
                continue
            filtered.append(name)
        for idx, name in enumerate(filtered):
            path = os.path.join(dir_path, name)
            is_last = idx == len(filtered) - 1
            connector = "└── " if is_last else "├── "
            lines.append(prefix + connector + name)
            if os.path.isdir(path):
                new_prefix = prefix + ("    " if is_last else "│   ")
                inner(path, new_prefix)

    lines.append(".")
    inner(root, "")
    return "\n".join(lines)


def find_files(root: str, extensions: list[str] | None, exclude_patterns: list[str] | None) -> list[str]:
    """Find files in the project directory matching specified extensions and excluding patterns.

    Args:
        root (str): Path to the project directory.
        extensions (list[str] | None): List of file extensions to include.
        exclude_patterns (list[str] | None): List of patterns to exclude.

    Returns:
        list[str]: List of matching file paths relative to the project directory.
    """
    matches = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir == os.curdir:
            rel_dir = ""
        # prune directories (skip hidden, generated, and excluded)
        pruned = []
        for d in dirnames:
            # skip hidden, generated, and default-excluded dirs
            if d.startswith((".", "generated_")) or d == "__pycache__" or d.endswith(".egg-info"):
                continue
            rel = os.path.join(rel_dir, d) if rel_dir else d
            if exclude_patterns and any(fnmatch.fnmatch(rel, pat) for pat in exclude_patterns):
                continue
            pruned.append(d)
        dirnames[:] = pruned
        # collect files, skipping hidden and excluded
        for fname in sorted(filenames):
            # skip hidden, generated, and default-excluded files
            if fname.startswith((".", "generated_")) or fname.endswith((".lock", ".egg-info")):
                continue
            rel = os.path.join(rel_dir, fname) if rel_dir else fname
            if exclude_patterns and any(fnmatch.fnmatch(rel, pat) for pat in exclude_patterns):
                continue
            if extensions and os.path.splitext(fname)[1] not in extensions:
                continue
            matches.append(rel)
    return matches


def fence_language(ext: str) -> str:
    """Map file extensions to Markdown fence languages.

    Args:
        ext (str): File extension.

    Returns:
        str: Corresponding fence language.
    """
    mapping = {".py": "python", ".md": "markdown", ".json": "json", ".yaml": "yaml", ".yml": "yaml"}
    return mapping.get(ext.lower(), "")


def make_anchor(text: str) -> str:
    """Create a Markdown anchor from a given text.

    Args:
        text (str): Text to convert to an anchor.

    Returns:
        str: Anchor string.
    """
    norm = unicodedata.normalize("NFKD", text)
    ascii_text = norm.encode("ascii", "ignore").decode("ascii")
    anchor = ascii_text.lower().replace(" ", "-")
    return "".join(c for c in anchor if c.isalnum() or c == "-")


@click.command()
@click.option(
    "--input-dir",
    "-i",
    default=".",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Dossier racine du projet",
)
@click.option(
    "--output-file",
    "-o",
    default="project.md",
    type=click.Path(dir_okay=False, writable=True),
    help="Fichier Markdown généré",
)
@click.option("--with-deps/--no-deps", default=True, help="Afficher la liste des dépendances")
@click.option("--with-tree/--no-tree", default=True, help="Afficher l'arborescence du projet")
@click.option(
    "--extensions", "-e", default=".py,.md,.yaml,.json", help="Extensions à inclure (séparées par des virgules)"
)
@click.option("--mode", type=click.Choice(["light", "full"]), default="full", help="Mode d'extraction")
@click.option("--max-snippet-lines", type=int, default=None, help="Nombre maximal de lignes par extrait")
@click.option("--exclude", "-x", default="", help="Motifs de fichiers ou dossiers à ignorer (séparés par des virgules)")
def main(  # noqa: PLR0912, PLR0913, PLR0914, PLR0915, PLR0917
    input_dir: str,
    output_file: str,
    with_deps: bool,  # noqa: FBT001
    with_tree: bool,  # noqa: FBT001
    extensions: str,
    mode: Literal["light", "full"],
    max_snippet_lines: int,
    exclude: str,
) -> None:
    """Génère un fichier Markdown documentant la structure et le contenu d'un projet."""
    input_dir = os.path.abspath(input_dir)
    meta = get_metadata(input_dir)
    project_name = meta["name"]
    version = meta["version"]
    author = meta["author"]
    dependencies = meta["dependencies"]
    # Default patterns to ignore: lock files, __pycache__ dirs, egg-info dirs
    default_excludes = ["*.lock", "*__pycache__*", "*.egg-info*"]
    user_excludes = [p for p in (exclude.split(",") if exclude else []) if p]
    ex_patterns = default_excludes + user_excludes
    ext_list: list[str] = [e if e.startswith(".") else f".{e}" for e in (extensions.split(",") if extensions else [])]

    # Ensure generated output file is prefixed to avoid self-inclusion
    dir_name, base_name = os.path.split(output_file)
    prefixed_base = f"generated_{base_name}"
    output_file = os.path.join(dir_name, prefixed_base) if dir_name else prefixed_base

    today = datetime.date.today().strftime("%Y-%m-%d")  # noqa: DTZ011
    toc_sections = []
    toc_sections.append("Arborescence du projet")
    if with_deps and mode == "full":
        toc_sections.append("Dépendances du projet")
    toc_sections.append("Fichiers détaillés")

    tree_str = generate_tree(input_dir, ex_patterns) if with_tree else ""

    if mode == "full":
        file_list = find_files(input_dir, ext_list, ex_patterns)
    else:
        readme_path = os.path.join(input_dir, "README.md")
        file_list = ["README.md"] if os.path.isfile(readme_path) else []

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(f'project_name: "{project_name}"\n')
        f.write(f'version: "{version}"\n')
        f.write(f'author: "{author}"\n')
        f.write(f'date_generated: "{today}"\n')
        f.write("---\n\n")
        f.write(f"# {project_name}\n\n")
        f.write(f"> **Version** : {version}  \n")
        f.write(f"> **Auteur** : {author}\n\n")
        f.write("---\n\n")
        f.write("## Table des matières\n\n")
        for idx, sec in enumerate(toc_sections, start=1):
            anchor = make_anchor(sec)
            f.write(f"{idx}. [{sec}](#{anchor})\n")
        f.write("\n---\n\n")
        if with_tree:
            f.write("## Arborescence du projet\n\n")
            f.write("```text\n")
            f.write(tree_str + "\n")
            f.write("```\n\n")
            if with_deps and mode == "full":
                f.write("---\n\n")
        if with_deps and mode == "full":
            f.write("## Dépendances du projet\n\n")
            f.write("```text\n")
            if dependencies:
                f.writelines(f"- {dep}\n" for dep in dependencies)
            else:
                f.write("- Aucune dépendance\n")
            f.write("```\n\n")
            f.write("---\n\n")
        f.write("## Fichiers détaillés\n\n")
        for idx, rel in enumerate(file_list):
            full_path = os.path.join(input_dir, rel)
            f.write(f"### `{rel}`\n\n")
            # Determine file extension and language for fencing
            ext: str = os.path.splitext(rel)[1].lower()
            lang = fence_language(ext)
            # Use four backticks for markdown files to avoid conflicts with inner backticks
            backticks = 5 if ext == ".md" else 3
            fence_open = "`" * backticks + (lang or "")
            fence_close = "`" * backticks
            f.write(f"{fence_open}\n")
            try:
                text = Path(full_path).read_text(encoding="utf-8", errors="ignore")
                lines = text.splitlines()
            except Exception:
                lines = []

            if max_snippet_lines is not None and len(lines) > max_snippet_lines:
                total = len(lines)
                lines = lines[:max_snippet_lines]
                lines.append(f"... (truncated {total - max_snippet_lines} lines)")
            f.write("\n".join(lines) + "\n")
            f.write(f"{fence_close}\n")
            if idx != len(file_list) - 1:
                f.write("\n---\n\n")
    click.echo(f"Markdown généré: {output_file}")
