from typing import Optional
from typer import Typer
import typer

from vrz.core import Poetry, Git, VersionSubstitution

def main():
    poetry = Poetry()
    git = Git()
    version_substitution = VersionSubstitution()
    
    app = Typer(
        no_args_is_help=True, 
        help="vrz simplifies versioning and releases of software packages. Created primarily for Python, but can be used with other language platforms as well."
        )

    @app.command()
    def minor(update_file: Optional[list[str]] = typer.Option(default=None)):
        old_version = poetry.version_read()
        poetry.version_bump_minor()
        typer.echo(f"Version bumped to {poetry.version_read()}.")

        if git.is_git_repo():
            tag_name = f"v{poetry.version_read()}"

            git.add("pyproject.toml")
            git.commit(f"Released {tag_name}.")
            git.push()
            typer.echo("Pushed updated pyproject.toml.")

            git.create_tag(tag_name)
            git.push_tag(tag_name)
            typer.echo(f"Git tag {tag_name} created and pushed.")

        if update_file:
            for file in update_file:
                typer.echo(f"Updating version in file: {file}")
                version_substitution.replace_version(file, old_version, poetry.version_read())
                git.add(file)
            git.commit(f"Updated version to {poetry.version_read()}.")
            git.push()
            typer.echo("Pushed updated files.")

        if poetry.is_current_project_published():
            typer.echo("Publishing package to PyPI.")
            poetry.publish()
            typer.echo("Publishing to PyPI done.")

    @app.command()
    def latest():
        """Get the latest version of the package."""
        typer.echo(poetry.version_read())

    app()

if __name__ == "__main__":
    main()
