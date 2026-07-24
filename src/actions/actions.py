import os
import subprocess
import tempfile
import wave

import numpy as np
import sounddevice as sd
from colorama import Fore, Style

from src.config.config import AGENDA_PATH, SAMPLE_RATE, WHISPER_LANG, whisper_model, AGENT_NAME


def open_app(params: dict) -> str:
    """
    Ação de abrir um programa ou aplicativo
    """

    # Aplicações permitdas
    APPS_PERMITIDOS = {
        "firefox": ["firefox"],
        "arquivos": ["dolphin"],
        "terminal": ["konsole"],
        "editor": ["code"],
        "zed": ["zed"],
        "intellij": ["idea"],
        "webstorm": ["webstorm"],
        "pycharm": ["pycharm"],
        "thunderbird": ["thunderbird"],
        "configuracoes": ["systemsettings"],
        "kamoso": ["kamoso"],
        "kcalc": ["kcalc"],
        "lutris": ["lutris"],
        "kalm": ["kalm"]
    }

    # Apelidos ou sinônimos que o modelo LLM deve endenter
    APELIDOS = {
        "editor com z": "zed", "editor z": "zed", "z": "zed", "aquele editor rápido": "zed",
        "aquele editor rapido": "zed",
        "editor padrao": "zed", "editor padrão": "zed",
        "code": "editor", "vscode": "editor", "vs code": "editor",
        "ide java": "intellij", "ide kotlin": "intellij", "idea": "intellij",
        "ide python": "pycharm",
        "ide web": "webstorm",
        "email": "thunderbird", "e-mail": "thunderbird",
        "configuracoes do sistema": "configuracoes", "configurações do sistema": "configuracoes",
        "ajustes": "configuracoes", "settings": "configuracoes",
        "webcam": "kamoso", "camera": "kamoso", "câmera": "kamoso",
        "calculadora": "kcalc",
        "jogos": "lutris", "launcher de jogos": "lutris", "gerenciador de jogos": "lutris",
        "respiracao": "kalm", "se acalmar": "kalm", "meditar": "kalm", "respirar": "kalm",
        "relaxar": "kalm", "desestressar": "kalm", "respiração": "kalm"
    }

    nome = params.get("nome", "").strip().lower()
    nome = APELIDOS.get(nome, nome)

    if nome not in APPS_PERMITIDOS:
        return f"Não tenho permissão para abrir '{nome}'."
    subprocess.Popen(APPS_PERMITIDOS[nome], start_new_session=True)
    return f"Abrindo {nome}."


def read_schedule(params: dict) -> str:
    """
    Realiza uma leitura do arquivo de agenda
    """

    if not os.path.exists(AGENDA_PATH):
        return "Você ainda não tem nada na agenda."
    with open(AGENDA_PATH, "r", encoding="utf-8") as file:
        linhas = [linha.strip() for linha in file if linha.strip()]
    if not linhas:
        return "Agenda vazia."
    return "Seus compromissos: " + "; ".join(linhas)


def create_item_on_schedule(params: dict) -> str:
    """
    Cria um item na agenda
    """

    texto = params.get("texto", "").strip()
    if not texto:
        return "Não entendi o que adicionar."
    with open(AGENDA_PATH, "a", encoding="utf-8") as f:
        f.write(texto + "\n")
    return f"Adicionado à agenda: {texto}"


def remove_item_from_schedule(params: dict) -> str:
    if not os.path.exists(AGENDA_PATH):
        return "Agenda já está vazia."

    with open(AGENDA_PATH, mode="r", encoding="utf-8") as f:
        linhas = [linha.strip() for linha in f if linha.strip()]

    if not linhas:
        return "Agenda já está vazia."

    indice = params.get("indice")

    if indice is None:
        return "Preciso do número do item para remover. Peça para ler a agenda primeiro."

    try:
        indice = int(indice)
    except (TypeError, ValueError):
        return "Número de item inválido."

    if indice < 1 or indice > len(linhas):
        return f"Não existe item número {indice}. Você tem {len(linhas)} compromisso(s)."

    removido = linhas.pop(indice - 1)

    with open(AGENDA_PATH, mode="w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + ("\n" if linhas else ""))

    return f"Removido: {removido}"


def record_audio() -> str:
    """
    Gravar um áudio
    """
    print(f"\n{Fore.YELLOW}[Pressione ENTER para começar a falar]{Style.RESET_ALL}")
    input()
    print(f"{Fore.YELLOW}Gravando... pressione ENTER de novo para parar.{Style.RESET_ALL}")

    frames = []

    def callback(indata, frame_count, time_info, status):
        frames.append(indata.copy())

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16",
        callback=callback()
    )

    with stream:
        input()  # Segunda vez que apertar ENTER, para parar a gravação

    audio = np.concatenate(frames, axis=0)

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)

    with wave.open(tmp.name, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())
    return tmp.name

def transcribe(path_wave: str) -> str:
    """
    Faz a transcrição do áudio
    """

    segments, _ = whisper_model.transcribe(path_wave, language=WHISPER_LANG)
    texto = " ".join(seg.text.strip() for seg in segments)
    os.unlink(path_wave)
    return texto.strip()


# def ask(user_text: str) -> str:

def speak(text: str):
    print(f"{Fore.CYAN}{AGENT_NAME}: {text}{Style.RESET_ALL}")
    tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name

    subprocess.run([
        "piper", "--model",
    ])