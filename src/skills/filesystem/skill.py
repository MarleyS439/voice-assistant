from helpers.filesystem import FileSystemHelper
from skills.base import Skill


class FileSystem(Skill):
    @property
    def name(self) -> str:
        return "FileSystem"

    @property
    def description(self) -> str:
        return (
            "Gerencia arquivos e diretórios: lista, pesquisa, "
            "lê, cria, copia, move, renomeia e exclui itens."
        )

    @property
    def execute(self, **kwargs):
        action = kwargs.get("action")

        if not action:
            raise ValueError("Ação não listada")

        if action == "list_directory":
            return FileSystemHelper.list_directory(path=kwargs["path"])

        return None
