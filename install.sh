#!/bin/bash

echo -e "\e[34mIniciando instalação...\e[0m"

# Atualizar todos os pacotes
sudo pacman --sync --refresh --sysupgrade --noconfirm

# Instalar o Ollama
echo -e "\e[34m[1/X] - Instalando pacotes necessários...\e[0m"
sudo pacman -S ollama python-pip portaudio

# Habilitar o serviço do Ollama
echo -e "\e[34m[2/X] - Habilitando o serviço...\e[0m"
sudo systemctl enable --now ollama

# Instalar modelo LLM - qwen2.5:3b-instruct
echo -e "\e[34m[3/X] - Instalando modelo...\e[0m"
ollama pull qwen2.5:3b-instruct

# Criando diretório para o assistente
echo -e "\e[34m[4/X] - Configurando...\e[0m"
mkdir -p ~/.programas/ai-model
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cp -r "$SCRIPT_DIR"/* ~/.programas/ai-model/
cd ~/.programas/ai-model
python -m venv .venv
source .venv/bin/activate
pip install faster-whisper sounddevice numpy piper-tts requests

# Instalar modelos de voz
echo -e "\e[34mInstalando modelos de voz...\e[0m"
mkdir -p ~/.local/share/piper-voices
cd ~/.local/share/piper-voices
curl -LO https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx
curl -LO https://huggingface.co/rhasspy/piper-voices/resolve/main/pt/pt_BR/faber/medium/pt_BR-faber-medium.onnx.json

# Habilita o descarregamento do modelo após 5 min
sudo mkdir -p /etc/systemd/system/ollama.service.d
echo -e "[Service]\nEnvironment=\"OLLAMA_KEEP_ALIVE=5m\"" | sudo tee /etc/systemd/system/ollama.service.d/override.conf

# Recarrega o daemon do systemctl
sudo systemctl daemon-reload

# Reinicia o serviço do ollama
sudo systemctl restart ollama
