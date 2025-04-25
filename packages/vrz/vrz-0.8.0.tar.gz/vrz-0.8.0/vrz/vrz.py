import shlex
import subprocess
from typer import Typer
import typer

class Poetry:
    def version_bump_minor(self):
        output = subprocess.run(
            shlex.split("poetry version minor"),
            check=True,
            capture_output=True,
            text=True,
        )
    
    def version_read(self):
        output = subprocess.run(
            shlex.split("poetry version -s"),
            check=True,
            capture_output=True,
            text=True,
        )
        return output.stdout.strip()

class Git:
    def is_git_repo(self):
        try:
            subprocess.run(
                shlex.split("git rev-parse --is-inside-work-tree"),
                check=True,
                capture_output=True,
                text=True,
            )
            return True
        except subprocess.CalledProcessError:
            return False
        
    def create_tag(self, tag_name):
        subprocess.run(
            shlex.split(f"git tag {tag_name}"),
            check=True,
            capture_output=True,
            text=True,
        )

    def push_tag(self, tag_name):
        subprocess.run(
            shlex.split(f"git push origin {tag_name}"),
            check=True,
            capture_output=True,
            text=True,
        )

def main():
    poetry = Poetry()
    git = Git()
    app = Typer(no_args_is_help=True)

    @app.command()
    def minor():
        poetry.version_bump_minor()
        typer.echo(f"Version bumped to {poetry.version_read()}.")
        if git.is_git_repo():
            tag_name = f"v{poetry.version_read()}"
            git.create_tag(tag_name)
            git.push_tag(tag_name)
            typer.echo(f"Git tag {tag_name} created and pushed.")

    @app.command()
    def latest():
        typer.echo(poetry.version_read())

    app()

if __name__ == "__main__":
    main()