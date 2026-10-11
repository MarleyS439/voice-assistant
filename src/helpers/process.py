import csv
import getpass
import io
import sys
import psutil
import subprocess


class ProcessHelper:

    @staticmethod
    def start(command: str) -> subprocess.Popen:
        return subprocess.Popen(command)

    @staticmethod
    def find_by_name(name: str) -> dict[int, str]:
        target = name.lower()
        result = {}

        for proc in psutil.process_iter(["pid", "name"]):
            try:
                pinfo = proc.info
                pid = pinfo.get("pid")
                pname = pinfo.get("name")

                if pname and target in pname.lower():
                    result[pid] = pname
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return result

    @staticmethod
    def is_running(name_process: str) -> bool:
        return len(ProcessHelper.find_by_name(name_process)) > 0

    @staticmethod
    def terminate(pids: dict[int, str]):
        for pid in pids:
            process = psutil.Process(pid)
            process.terminate()

    @staticmethod
    def kill(pid: int):
        process = psutil.Process(pid)
        process.kill()

    @staticmethod
    def list() -> dict[int, str]:
        process = psutil.process_iter(["pid", "name", "username", "status"])
        proc = {}
        username = getpass.getuser()

        for p in process:
            if p.info["username"] == username:
                proc.update({
                    p.info["pid"]: {
                        "name": p.info["name"],
                        "status": p.info["status"]
                    }
                })
        return proc

    @staticmethod
    def to_csv(processes: dict[int, str]) -> str:
        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(["pid", "name", "status"])

        for pid, item in processes.items():
            writer.writerow([
                pid,
                item.get("name"),
                item.get("status")
            ])

        return output.getvalue()
