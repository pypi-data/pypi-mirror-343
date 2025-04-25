# vrz: Easy versioning and releases

`vrz` simplifies versioning and releases of software packages. Created primarily for Python, but can be used with other language platforms as well.

## Installation

In order to add `vrz` into your Poetry project, execute the following command:

```bash
poetry install --group=dev vrz
```

You can also install `vrz` globally using pipx:

```bash
pipx install vrz
```

## Usage

In order to release new minor version of your application, execute the `vrz minor` command:

```
$ vrz minor
Version bumped to 0.16.0.
Pushed updated pyproject.toml.
Git tag v0.16.0 created and pushed.
Publishing package to PyPI.
Publishing to PyPI done.
```

`vrz` will:
- bump your `pyproject.toml` project version (if Poetry project is detected)
- commit and push `pyproject.toml` (if Git repository is detected)
- publish package to PyPI (if current project is already present in PyPI index)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.