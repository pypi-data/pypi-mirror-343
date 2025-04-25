from pathlib import Path
import shlex
import subprocess
import requests as request


class Poetry:
    def __init__(self, working_dir: Path = None):
        self.working_dir = working_dir

    @classmethod
    def init_project(cls, path: Path = None):
        """
        Initializes a new Poetry project in the specified directory.
        If no path is provided, a temporary directory is created.

        Returns:
            Poetry: An instance of the Poetry class associated with the project directory.
        """
        if path is None:
            temp_dir = tempfile.TemporaryDirectory()
            project_path = Path(temp_dir.name)
            project_path._temp_dir = temp_dir
        else:
            project_path = Path(path)
            project_path.mkdir(parents=True, exist_ok=True)

        subprocess.run(
            shlex.split("poetry init -n"),
            check=True,
            capture_output=True,
            text=True,
            cwd=project_path,
        )

        return cls(working_dir=project_path)
    
    def version_bump_minor(self):
        subprocess.run(
            shlex.split("poetry version minor"),
            check=True,
            capture_output=True,
            text=True,
            cwd=self.working_dir,
        )

    def version_read(self):
        output = subprocess.run(
            shlex.split("poetry version -s"),
            check=True,
            capture_output=True,
            text=True,
            cwd=self.working_dir,
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
            cwd=self.working_dir,
        )
        return True

    def project_name(self):
        output = subprocess.run(
            shlex.split("poetry version"),
            check=True,
            capture_output=True,
            text=True,
            cwd=self.working_dir,
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


class VersionSubstitution:
    def replace_version(self, file_path: str, old_version: str, new_version: str):
        with open(file_path, "r") as file:
            content = file.read()

        new_content = content.replace(old_version, new_version)

        with open(file_path, "w") as file:
            file.write(new_content)
