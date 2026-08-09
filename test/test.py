import subprocess

def verificar_modelos() -> list[str]:
    """
    Verifica se há modelos de voz do piper disponíveis
    """

    # Lista de modelos de voz do piper
    modelos = []

    # Obtém o usuário
    usuario = subprocess.run(
        ["whoami"],
        capture_output=True,
        text=True
    )

    # Realiza uma listagem de itens no diretório do piper
    comando = subprocess.run(
        ["ls", f"/home/{usuario.stdout.strip()}/.local/share/piper-voices/"],
        capture_output=True,
        text=True
    )

    print(comando.stdout)

    # Valida e adiciona items na lista
    if comando.stdout is not None:
        itens = comando.stdout.splitlines()
        for item in itens:
            item = item.strip()
            if item.endswith(".onnx"):
                modelos.append(item)

    return modelos

def baixar_modelos(modelo: str) -> bool:
    """
    Baixa modelos de voz
    """

    # Valida se é necessário baixar modelos de voz
    if not verificar_modelos():



print(verificar_modelos())