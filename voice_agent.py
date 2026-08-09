#!/usr/bin/env python3
"""
Agente de voz local (CachyOS/Arch) - conversa + ações limitadas.

Pipeline: microfone -> faster-whisper (STT) -> Ollama (LLM) -> Piper (TTS) -> alto-falante

SEGURANÇA: o LLM nunca executa comandos livres. Ele só pode "chamar" funções
que estão explicitamente registradas em ACOES_PERMITIDAS. Qualquer coisa fora
disso é ignorada. Não há shell exec, não há acesso a arquivos fora do que
você mesmo programar aqui.
"""

import json
import subprocess
import sys
import wave
import tempfile
import os
from datetime import datetime

import numpy as np
import sounddevice as sd
import requests
from faster_whisper import WhisperModel
from colorama import init, Fore, Style

init(autoreset=True)

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO
# ---------------------------------------------------------------------------

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen2.5:3b-instruct"  # leve o suficiente pra 6-8GB de RAM livre, sem GPU

WHISPER_MODEL_SIZE = "base"   # tiny/base/small/medium (maior = mais preciso, mais lento)
WHISPER_LANG = "pt"

PIPER_VOICE = os.path.expanduser(
    "~/.local/share/piper-voices/pt_BR-faber-medium.onnx"
)

SAMPLE_RATE = 16000

# Caminho de um arquivo de agenda simples que você mesmo mantém.
# Uma linha por compromisso, ex: "2026-07-23 14:00 Reunião com orientador"
AGENDA_PATH = os.path.expanduser("~/.agenda.txt")

# ---------------------------------------------------------------------------
# WHITELIST DE AÇÕES — ESTE É O LIMITE DE PODER DO AGENTE.
# Adicione aqui só o que você realmente quer permitir. Nada além disso
# pode ser executado, não importa o que o modelo "decida".
# ---------------------------------------------------------------------------

def acao_abrir_app(params: dict) -> str:
    apps_permitidos = {
        "firefox": ["firefox"],
        "arquivos": ["dolphin"],
        "terminal": ["konsole"],
        "editor": ["code"],
        "zed": ["zed"],
        "intellij": ["idea"],
        "pycharm": ["pycharm"],
        "thunderbird": ["thunderbird"],
        "configuracoes": ["systemsettings"],
        "kamoso": ["kamoso"],
        "kate": ["kate"],
        "kcalc": ["kcalc"],
        "lutris": ["lutris"],
    }

    # Apelidos/sinônimos que o LLM (ou você) pode falar, mapeados pro nome canônico acima.
    # Se o LLM não mandar o nome exato, ainda tentamos casar por aqui antes de recusar.
    apelidos = {
        "editor com z": "zed", "editor z": "zed", "z": "zed",
        "aquele editor rapido": "zed", "aquele editor rápido": "zed",
        "code": "editor", "vscode": "editor", "vs code": "editor",
        "ide java": "intellij", "ide kotlin": "intellij", "idea": "intellij",
        "ide python": "pycharm",
        "email": "thunderbird", "e-mail": "thunderbird",
        "configuracoes do sistema": "configuracoes", "configurações do sistema": "configuracoes",
        "ajustes": "configuracoes", "settings": "configuracoes",
        "webcam": "kamoso", "camera": "kamoso", "câmera": "kamoso",
        "calculadora": "kcalc",
        "jogos": "lutris", "launcher de jogos": "lutris", "gerenciador de jogos": "lutris",
    }

    nome = params.get("nome", "").strip().lower()
    nome = apelidos.get(nome, nome)  # tenta traduzir apelido pro nome canônico

    if nome not in apps_permitidos:
        return f"Não tenho permissão para abrir '{nome}'."
    subprocess.Popen(apps_permitidos[nome], start_new_session=True)
    return f"Abrindo {nome}."


def acao_ler_agenda(params: dict) -> str:
    if not os.path.exists(AGENDA_PATH):
        return "Você ainda não tem nada na agenda."
    with open(AGENDA_PATH, "r", encoding="utf-8") as f:
        linhas = [l.strip() for l in f if l.strip()]
    if not linhas:
        return "Agenda vazia."
    return "Seus compromissos: " + "; ".join(linhas)


def acao_adicionar_agenda(params: dict) -> str:
    texto = params.get("texto", "").strip()
    if not texto:
        return "Não entendi o que adicionar."
    with open(AGENDA_PATH, "a", encoding="utf-8") as f:
        f.write(texto + "\n")
    return f"Adicionado à agenda: {texto}"


DIAS_SEMANA = {
    0: "segunda-feira", 1: "terça-feira", 2: "quarta-feira",
    3: "quinta-feira", 4: "sexta-feira", 5: "sábado", 6: "domingo",
}


def acao_hora_data(params: dict) -> str:
    agora = datetime.now()
    tipo = params.get("tipo", "ambos")  # "hora", "data" ou "ambos"

    hora_str = agora.strftime("%H:%M")
    data_str = f"{DIAS_SEMANA[agora.weekday()]}, {agora.strftime('%d/%m/%Y')}"

    if tipo == "hora":
        return f"Agora são {hora_str}."
    elif tipo == "data":
        return f"Hoje é {data_str}."
    else:
        return f"Agora são {hora_str}, {data_str}."


ACOES_PERMITIDAS = {
    "abrir_app": acao_abrir_app,
    "ler_agenda": acao_ler_agenda,
    "adicionar_agenda": acao_adicionar_agenda,
    "hora_data": acao_hora_data,
}

SYSTEM_PROMPT = f"""Você é um assistente de voz local, respondendo sempre em português do Brasil.

Você pode fazer duas coisas:
1. Responder normalmente em texto.
2. Pedir para executar UMA ação, respondendo SOMENTE com um JSON no formato:
   {{"acao": "nome_da_acao", "params": {{...}}}}

Ações disponíveis: {list(ACOES_PERMITIDAS.keys())}
- abrir_app: params={{"nome": "..."}}. Apps disponíveis e como reconhecer o pedido:
    - firefox: navegador de internet
    - arquivos: gerenciador de arquivos (Dolphin)
    - terminal: terminal/console (Konsole)
    - editor: VS Code, "editor de código" genérico
    - zed: editor de código chamado "Zed" (às vezes o usuário fala só "editor com Z" ou "aquele editor rápido")
    - intellij: IntelliJ IDEA, IDE de Java/Kotlin
    - pycharm: PyCharm, IDE de Python
    - thunderbird: cliente de e-mail
    - configuracoes: configurações do sistema/Plasma
    - kamoso: aplicativo de webcam/câmera
    - kate: editor de texto simples do KDE
    - kcalc: calculadora
    - lutris: gerenciador/launcher de jogos (o usuário pode falar só "jogos" ou "launcher de jogos")
    Se o usuário pedir algo vago (ex: "meu editor preferido"), use o contexto da conversa; se não tiver contexto suficiente, pergunte qual dos editores ele quer em vez de adivinhar.
- ler_agenda: params={{}}
- adicionar_agenda: params={{"texto": "descrição do compromisso"}}
- hora_data: params={{"tipo": "hora"|"data"|"ambos"}} (use quando o usuário perguntar as horas, o dia, ou ambos)

Se o pedido do usuário não corresponder a nenhuma ação, apenas responda normalmente em texto,
de forma curta e natural, como numa conversa falada. Nunca invente ações fora da lista.
"""

# ---------------------------------------------------------------------------
# STT
# ---------------------------------------------------------------------------

print("Carregando modelo Whisper (STT)...")
whisper_model = WhisperModel(WHISPER_MODEL_SIZE, device="cpu", compute_type="int8")


def gravar_audio() -> str:
    print(f"\n{Fore.YELLOW}[Pressione ENTER para começar a falar]{Style.RESET_ALL}")
    input()
    print(f"{Fore.YELLOW}Gravando... pressione ENTER de novo para parar.{Style.RESET_ALL}")

    frames = []

    def callback(indata, frame_count, time_info, status):
        frames.append(indata.copy())

    stream = sd.InputStream(
        samplerate=SAMPLE_RATE, channels=1, dtype="int16", callback=callback
    )
    with stream:
        input()  # segunda vez que aperta ENTER, para de gravar

    audio = np.concatenate(frames, axis=0)

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    with wave.open(tmp.name, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())
    return tmp.name


def transcrever(caminho_wav: str) -> str:
    segments, _ = whisper_model.transcribe(caminho_wav, language=WHISPER_LANG)
    texto = " ".join(seg.text.strip() for seg in segments)
    os.unlink(caminho_wav)
    return texto.strip()

# ---------------------------------------------------------------------------
# LLM (Ollama)
# ---------------------------------------------------------------------------

historico = [{"role": "system", "content": SYSTEM_PROMPT}]


def perguntar_llm(texto_usuario: str) -> str:
    historico.append({"role": "user", "content": texto_usuario})
    resposta = requests.post(
        OLLAMA_URL,
        json={"model": OLLAMA_MODEL, "messages": historico, "stream": False},
        timeout=120,
    )
    resposta.raise_for_status()
    conteudo = resposta.json()["message"]["content"]
    historico.append({"role": "assistant", "content": conteudo})
    return conteudo


def processar_resposta(conteudo: str) -> str:
    """Se for um JSON de ação, executa via whitelist. Senão, retorna o texto puro."""
    conteudo_strip = conteudo.strip()
    if conteudo_strip.startswith("{"):
        try:
            dados = json.loads(conteudo_strip)
            acao = dados.get("acao")
            params = dados.get("params", {})
            if acao in ACOES_PERMITIDAS:
                return ACOES_PERMITIDAS[acao](params)
            else:
                return f"Ação '{acao}' não é permitida."
        except json.JSONDecodeError:
            pass
    return conteudo_strip

# ---------------------------------------------------------------------------
# TTS (Piper)
# ---------------------------------------------------------------------------

def falar(texto: str):
    print(f"{Fore.CYAN}Agente: {texto}{Style.RESET_ALL}")
    tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    subprocess.run(
        ["piper", "--model", PIPER_VOICE, "--output_file", tmp_wav],
        input=texto.encode("utf-8"),
        check=True,
    )
    subprocess.run(["aplay", tmp_wav], check=True)
    os.unlink(tmp_wav)

# ---------------------------------------------------------------------------
# LOOP PRINCIPAL
# ---------------------------------------------------------------------------

def main():
    print("Agente de voz local pronto. Ctrl+C para sair.\n")
    try:
        while True:
            caminho = gravar_audio()
            texto_usuario = transcrever(caminho)
            if not texto_usuario:
                print("(nada entendido, tente de novo)")
                continue
            print(f"{Fore.GREEN}Você: {texto_usuario}{Style.RESET_ALL}")

            if texto_usuario.lower().strip() in ("sair", "encerrar", "tchau"):
                falar("Até mais!")
                break

            resposta_bruta = perguntar_llm(texto_usuario)
            resposta_final = processar_resposta(resposta_bruta)
            falar(resposta_final)

    except KeyboardInterrupt:
        print("\nEncerrado.")
        sys.exit(0)


if __name__ == "__main__":
    main()
