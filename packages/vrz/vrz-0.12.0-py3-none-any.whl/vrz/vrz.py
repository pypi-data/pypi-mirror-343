import shlex
import subprocess
from typer import Typer
import typer
import requests as request

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

    def is_published(self, package_name):
        url = f"https://pypi.org/pypi/{package_name}/json"
        response = request.get(url)
        return response.status_code != 404

    def is_current_project_published(self):
        project_name = self.project_name()
        return self.is_published(project_name)

    def publish(self):
        subprocess.run(
            shlex.split("poetry publish --build"),
            check=True,
            capture_output=True,
            text=True,
        )
        return True

    def project_name(self):
        output = subprocess.run(
            shlex.split("poetry version"),
            check=True,
            capture_output=True,
            text=True,
        )
        return output.stdout.split()[0].strip()

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

    def push(self):
        subprocess.run(
            shlex.split("git push"),
            check=True,
            capture_output=True,
            text=True,
        )

    def add(self, file: str):
        subprocess.run(
            shlex.split(f"git add {file}"),
            check=True,
            capture_output=True,
            text=True,
        )

    def commit(self, message: str):
        subprocess.run(
            shlex.split(f"git commit -m '{message}'"),
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

            git.add("pyproject.toml")
            git.commit(f"Released {tag_name}.")
            git.push()
            typer.echo("Pushed updated pyproject.toml.")

            git.create_tag(tag_name)
            git.push_tag(tag_name)
            typer.echo(f"Git tag {tag_name} created and pushed.")

        if poetry.is_current_project_published():
            typer.echo("Publishing package to PyPI.")
            poetry.publish()
            typer.echo("Publishing to PyPI done.")


    @app.command()
    def latest():
        typer.echo(poetry.version_read())

    app()

if __name__ == "__main__":
    main()