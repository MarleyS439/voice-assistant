from subprocess import Popen

from helpers.process import ProcessHelper
from skills.base import Skill


class Applications(Skill):

    @property
    def name(self) -> str:
        return "Aplicações"

    @property
    def description(self) -> str:
        return "Realiza procedimentos de abertura, fechamento e listagem de processos de aplicações"

    @property
    def execute(self, **kwargs) -> Popen | bool | str | None:
        action = str(kwargs.get("action"))
        application = str(kwargs.get("application"))

        if not action or not application:
            raise ValueError(
                "Os argumentos 'action' e 'application' são obrigatórios."
            )

        if action == "open":
            return ProcessHelper.start(command=application)
        elif action == "close":
            exists = ProcessHelper.is_running(name_process=application)
            if exists:
                processes = ProcessHelper.find_by_name(name=application)
                ProcessHelper.terminate(processes)
                return bool(processes)
            else:
                print("Processo não está em execução")
        elif action == "verify":
            return ProcessHelper.to_csv(processes=ProcessHelper.list())
        else:
            print("Ação não integrada. Tente 'open', 'close' ou 'verify'")
        return None
