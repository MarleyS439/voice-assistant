"""Janela principal do assistente de voz — PySide6.

Layout minimalista:
- Área de texto com a conversa (somente leitura)
- Botão push-to-talk (clica para gravar, clica de novo para parar)
- Label de status (Ocioso / Gravando / Processando / Falando)

O processamento (transcrição + LLM + TTS) roda em QThread
para não congelar a UI.
"""

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QTextEdit, QLabel,
)

from agent.voice_agent import VoiceAgent


class TurnWorker(QThread):
    """Worker que executa transcrição + LLM + dispatch em background."""

    finished = Signal(str)   # resposta final do agente
    error = Signal(str)      # mensagem de erro

    def __init__(self, agent: VoiceAgent, wav_path: str):
        super().__init__()
        self._agent = agent
        self._wav_path = wav_path

    def run(self):
        try:
            # 1. Transcrever
            user_text = self._agent._stt.transcribe(self._wav_path)
            if not user_text:
                self.finished.emit("")
                return

            # 2. Processar (LLM + dispatch)
            response = self._agent.process_turn(user_text)

            # 3. Falar
            self._agent.speak(response)

            self.finished.emit(user_text + "\n" + response)
        except Exception as e:
            self.error.emit(str(e))


class MainWindow(QMainWindow):

    def __init__(self, agent: VoiceAgent):
        super().__init__()
        self._agent = agent
        self._worker: TurnWorker | None = None
        self._recording = False

        self.setWindowTitle("Assistente de Voz Local")
        self.setMinimumSize(420, 320)

        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setSpacing(12)

        # Área de conversa
        self._chat = QTextEdit()
        self._chat.setReadOnly(True)
        self._chat.setPlaceholderText("A conversa aparecerá aqui...")
        layout.addWidget(self._chat)

        # Status
        self._status = QLabel("Ocioso")
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._status.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(self._status)

        # Botão push-to-talk
        self._btn = QPushButton("🎙  Falar")
        self._btn.setFixedHeight(56)
        self._btn.setStyleSheet(
            "QPushButton { font-size: 18px; border-radius: 8px; }"
            "QPushButton:!pressed { background-color: #3daee9; color: white; }"
            "QPushButton:pressed  { background-color: #2980b9; color: white; }"
        )
        self._btn.clicked.connect(self._on_button)
        layout.addWidget(self._btn)

    # ── Botão ────────────────────────────────────────────────────────────────

    def _on_button(self):
        if self._worker is not None:
            # Processando, ignora cliques
            return

        if not self._recording:
            # Iniciar gravação
            try:
                self._agent._stt.start_recording()
                self._recording = True
                self._status.setText("🔴 Gravando — clique novamente para parar")
                self._status.setStyleSheet("color: #e74c3c; font-size: 12px;")
                self._btn.setText("⏹  Parar")
                self._btn.setStyleSheet(
                    "QPushButton { font-size: 18px; border-radius: 8px; }"
                    "QPushButton:!pressed { background-color: #e74c3c; color: white; }"
                    "QPushButton:pressed  { background-color: #c0392b; color: white; }"
                )
            except Exception as e:
                self._status.setText(f"Erro: {e}")
        else:
            # Parar gravação e processar
            wav_path = self._agent._stt.stop_recording()
            self._recording = False
            self._btn.setText("🎙  Falar")
            self._btn.setEnabled(False)
            self._btn.setStyleSheet(
                "QPushButton { font-size: 18px; border-radius: 8px; }"
                "QPushButton:!pressed { background-color: #3daee9; color: white; }"
                "QPushButton:pressed  { background-color: #2980b9; color: white; }"
            )

            if not wav_path:
                self._status.setText("Ocioso")
                self._status.setStyleSheet("color: #888; font-size: 12px;")
                self._btn.setEnabled(True)
                return

            self._status.setText("⏳ Processando...")
            self._status.setStyleSheet("color: #f39c12; font-size: 12px;")

            # Processar em thread separada
            self._worker = TurnWorker(self._agent, wav_path)
            self._worker.finished.connect(self._on_turn_finished)
            self._worker.error.connect(self._on_turn_error)
            self._worker.start()

    def _on_turn_finished(self, conversation: str):
        """Chamado quando o worker termina com sucesso."""
        if conversation:
            user_text, _, agent_text = conversation.partition("\n")
            self._chat.append(f"<b>Você:</b> {user_text}")
            self._chat.append(f"<b>Agente:</b> {agent_text}")
            self._chat.append("")

        self._worker = None
        self._btn.setEnabled(True)
        self._status.setText("Ocioso")
        self._status.setStyleSheet("color: #888; font-size: 12px;")

    def _on_turn_error(self, message: str):
        """Chamado quando o worker encontra um erro."""
        self._chat.append(f"<i style='color:red'>Erro: {message}</i>")
        self._chat.append("")
        self._worker = None
        self._btn.setEnabled(True)
        self._status.setText("Ocioso")
        self._status.setStyleSheet("color: #888; font-size: 12px;")
