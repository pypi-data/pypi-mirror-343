import os
import subprocess
from pathlib import Path
import pytest
from click.testing import CliRunner

from proj2md.cli import generate_tree, find_files, get_metadata, main


def test_generate_tree_and_find_files(tmp_path):
    # Create directory structure with various files
    (tmp_path / 'a.py').write_text("print(1)")
    (tmp_path / 'generated_b.py').write_text("print(2)")
    (tmp_path / '__pycache__').mkdir()
    (tmp_path / '__pycache__' / 'x.pyc').write_text('junk')
    (tmp_path / 'c.lock').write_text('')
    sub = tmp_path / 'sub'
    sub.mkdir()
    (sub / 'c.py').write_text("print(3)")
    (sub / 'generated_d.py').write_text("print(4)")

    # generate tree and files list without custom excludes
    tree = generate_tree(str(tmp_path), exclude_patterns=None)
    lines = tree.splitlines()
    # Should include a.py and sub, but not generated_* or __pycache__ or lock files
    assert any('a.py' in line for line in lines)
    assert any('sub' in line for line in lines)
    assert not any('generated_b.py' in line for line in lines)
    assert not any('c.lock' in line for line in lines)

    files = find_files(str(tmp_path), ['.py'], exclude_patterns=None)
    assert 'a.py' in files
    assert 'sub/c.py' in files
    assert 'generated_b.py' not in files
    assert 'sub/generated_d.py' not in files


def test_get_metadata_default(tmp_path, monkeypatch):
    # Without pyproject.toml, name should be directory name, version empty, author empty or from git
    name = tmp_path.name
    # Monkeypatch subprocess.run in proj2md.cli to simulate no git config
    monkeypatch.setattr(
        'proj2md.cli.subprocess.run',
        lambda *args, **kwargs: subprocess.CompletedProcess(args, 0, stdout='')
    )
    meta = get_metadata(str(tmp_path))
    assert meta['name'] == name
    assert meta['version'] == ''
    # No authors, so author string is empty
    assert meta['author'] == ''


def test_get_metadata_from_pyproject(tmp_path):
    # Create a valid pyproject.toml with project metadata
    content = (
        '[project]\n'
        'name = "testproj"\n'
        'version = "1.2.3"\n'
        'dependencies = ["dep1>=0.1"]\n'
        'authors = [{name = "Alice"}]\n'
    )
    (tmp_path / 'pyproject.toml').write_text(content)
    meta = get_metadata(str(tmp_path))
    assert meta['name'] == 'testproj'
    assert meta['version'] == '1.2.3'
    assert 'Alice' in meta['author']
    assert 'dep1' in meta['dependencies']


def test_cli_main_creates_file(tmp_path):
    # Prepare a minimal project directory
    (tmp_path / 'a.py').write_text("print('hello')")
    # Create pyproject.toml for metadata
    pyproject = tmp_path / 'pyproject.toml'
    pyproject.write_text(
        '[project]\n'
        'name = "cli_test"\n'
        'version = "0.0.1"\n'
        'authors = [{name = "Bob"}]\n'
    )
    runner = CliRunner()
    # Run CLI: output-file doc.md -> actual generated file is generated_doc.md
    # Invoke CLI, specifying absolute paths (cwd unchanged)
    output_arg = str(tmp_path / 'doc.md')
    result = runner.invoke(
        main,
        ['-i', str(tmp_path), '-o', output_arg, '--no-tree', '--no-deps'],
    )
    assert result.exit_code == 0
    gen_file = tmp_path / 'generated_doc.md'
    assert gen_file.exists(), "Generated file should be prefixed with 'generated_'"
    content = gen_file.read_text()
    # Check front-matter and file details
    assert 'project_name: "cli_test"' in content
    assert 'version: "0.0.1"' in content
    assert 'Bob' in content
    assert '### `a.py`' in content
