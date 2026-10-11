#!/usr/bin/env python3
import sys
from colorama import Fore, Style

from actions.interaction import Interaction


def main() -> None:
    """"""

    print(Fore.LIGHTGREEN_EX + "Agente de voz local pronto. Ctrl+C para sair.\n" + Style.RESET_ALL)

    try:
        while True:
            path = Interaction.record()
            user_text = Interaction.transcribe(path_wav=path)
            if not user_text:
                print(f"{Fore.YELLOW}(Nada entendido, tente de novo)")
                continue
            print(f"{Fore.LIGHTGREEN_EX}Você: {user_text}{Style.RESET_ALL}")

            if user_text.lower().strip() in ("sair", "encerrar", "thau"):
                Interaction.talk("Até mais!")
                break

            raw_response = Interaction.ask(user_text)
            final_response = Interaction.process(raw_response)
            Interaction.talk(final_response)

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nEncerrando..." + Style.RESET_ALL)
        sys.exit(0)


if __name__ == "__main__":
    main()
