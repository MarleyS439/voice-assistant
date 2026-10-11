import subprocess
from pathlib import Path


class FileSystemHelper:

    @staticmethod
    def list_directory(path: str):
        directory = Path(path).expanduser()

        if not directory.exists():
            raise NotADirectoryError(path)

        if not directory.is_dir():
            raise NotADirectoryError(path)

        return [
            {
                "name": item.name,
                "path": str(item),
                "is_directory": item.is_dir(),
                "is_file": item.is_file(),
            }
            for item in directory.iterdir()
        ]

    @staticmethod
    def get_file_info():
        ...

    @staticmethod
    def exists(path: str) -> bool:
        return Path(path).expanduser().exists()

    @staticmethod
    def search():
        ...

    @staticmethod
    def read_file():
        ...

    @staticmethod
    def create_directory():
        ...

    @staticmethod
    def create_file():
        ...

    @staticmethod
    def write_file():
        ...

    @staticmethod
    def rename():
        ...

    @staticmethod
    def copy():
        ...

    @staticmethod
    def move():
        ...

    @staticmethod
    def delete_file():
        ...

    @staticmethod
    def delete_directory():
        ...
