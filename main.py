from colorama import Fore, Style
from faster_whisper import WhisperModel
from src.config.config import WHISPER_MODEL_SIZE
from src.actions.actions import record_audio, transcribe


def main():
    """
    Loop principal
    """

    # Carrega o modelo do Whisper
    whisper_model = WhisperModel(
        WHISPER_MODEL_SIZE,
        device="cpu",
        compute_type="int8"
    )

    print("Agente de voz local pronto. Ctrl+C para sair.\n")

    try:
        while True:
            path = record_audio()
            texto_usuario = transcribe(path)
            if not texto_usuario:
                print("(nada entendido, tente de novo)")
                continue
            print(f"{Fore.GREEN}Você: {texto_usuario}{Style.RESET_ALL}")

            if texto_usuario.lower().strip() in ("sair", "encerrar", "tchau"):
                speak("Até mais!")
                break

if __name__ == "__main__":
    main()