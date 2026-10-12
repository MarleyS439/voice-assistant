"""Text-to-Speech usando Piper.

Recebe texto, gera áudio via Piper e reproduz via aplay.
"""

import os
import subprocess
import tempfile

from config.settings import PIPER_VOICE


class TTS:
    """Fachada para síntese de voz via Piper + aplay."""

    def __init__(self):
        self._voice = PIPER_VOICE

    def speak(self, text: str) -> None:
        """Sintetiza e reproduz o texto em voz alta."""
        tmp_wav = tempfile.NamedTemporaryFile(
            suffix=".wav", delete=False
        ).name
        try:
            subprocess.run(
                ["piper", "--model", self._voice, "--output_file", tmp_wav],
                input=text.encode("utf-8"),
                check=True,
            )
            subprocess.run(["aplay", tmp_wav], check=True)
        finally:
            if os.path.exists(tmp_wav):
                os.unlink(tmp_wav)
