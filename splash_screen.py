from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PySide6.QtGui import QPainter, QColor, QFont, QLinearGradient, QBrush, QPen, QPixmap
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, Property
import json
import os
import sys

def get_resource_path(relative_path):
    """Obtém o caminho correto para recursos, seja em desenvolvimento ou no executável"""
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Se não estiver rodando no executável, usa o diretório atual
        base_path = os.path.abspath(".")
    
    full_path = os.path.join(base_path, relative_path)
    
    # Verificar se o arquivo existe
    if not os.path.exists(full_path):
        # Se não existir, tentar no diretório atual (para desenvolvimento)
        full_path = os.path.join(os.path.abspath("."), relative_path)
    
    return full_path

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        
        # Carregar configurações (opcional)
        self.load_config()
        
        # Título dinâmico baseado na empresa
        empresa_nome = self.config.get('empresa_nome', 'Sua Empresa')
        self.setWindowTitle(empresa_nome)
        self.setFixedSize(800, 500)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Cores principais (Padrão VTEX)
        self.primary_color = QColor(233, 30, 99)   # Rosa VTEX
        self.text_color = QColor(33, 33, 33)       # Quase preto
        
        # Cor do brilho fixa
        self.glow_color = QColor('#E91E63')  # Rosa VTEX brilhante

        self._glow_value = 0
        self.init_ui()
        self.init_animations()
    
    def load_config(self):
        """Carrega configurações da splash screen (opcional)"""
        try:
            with open('empresa_config.json', 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                self.config = config_data.get('splash_screen', {})
                # Adicionar nome da empresa
                self.config['empresa_nome'] = config_data.get('empresa', {}).get('nome', 'Sua Empresa')
        except:
            # Se não conseguir carregar, usar configurações padrão (vazias)
            self.config = {'empresa_nome': 'Sua Empresa'}

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(40, 40, 40, 40)
        self.setLayout(layout)

        self.container = QWidget(self)
        self.container.setFixedSize(600, 350)
        self.container.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
        """)

        container_layout = QVBoxLayout(self.container)
        container_layout.setAlignment(Qt.AlignCenter)
        container_layout.setContentsMargins(70, 70, 70, 70)

        # Logo VTEX
        self.logo = QLabel()
        logo_path = get_resource_path("VTEX_Logo.svg.png")
        
        # Verificar se a imagem existe antes de carregar
        if os.path.exists(logo_path):
            self.logo.setPixmap(QPixmap(logo_path).scaled(120, 40, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            # Se a imagem não existir, criar um texto como fallback
            self.logo.setText("VTEX")
            self.logo.setFont(QFont("Segoe UI", 16, QFont.Bold))
            self.logo.setStyleSheet(f"color: {self.primary_color.name()};")
        
        self.logo.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.logo)
        
        container_layout.addSpacing(20)

        # TEXTO DEPOIS - Subtítulo
        subtitle = QLabel("VTEX Freight Calculator")
        subtitle.setFont(QFont("Segoe UI", 16, QFont.Medium))
        subtitle.setStyleSheet(f"color: {self.text_color.name()}; letter-spacing: 2px;")
        subtitle.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(subtitle)

        container_layout.addSpacing(30)

        # Mensagem
        self.label = QLabel("Iniciando experiência premium")
        self.label.setFont(QFont("Segoe UI", 12))
        self.label.setStyleSheet(f"color: {self.text_color.name()};")
        self.label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.label)

        # Barra de progresso
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(8)
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                background-color: rgba(0, 0, 0, 0.05);
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background-color: {self.primary_color.name()};
                border-radius: 4px;
            }}
        """)
        container_layout.addWidget(self.progress)

        # Porcentagem
        self.percentage = QLabel("0%")
        self.percentage.setFont(QFont("Segoe UI", 10))
        self.percentage.setStyleSheet(f"color: {self.text_color.name()};")
        self.percentage.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.percentage)

        # Status
        self.status = QLabel("Carregando API de consulta...")
        self.status.setFont(QFont("Segoe UI", 10))
        self.status.setStyleSheet(f"color: {self.text_color.name()};")
        self.status.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(self.status)

        layout.addWidget(self.container)

    def init_animations(self):
        # Brilho pulsante
        self.glow_anim = QPropertyAnimation(self, b"glow_value")
        self.glow_anim.setDuration(3000)  # Reduzido de 4000 para 2000ms (mais rápido)
        self.glow_anim.setStartValue(0)
        self.glow_anim.setEndValue(1)
        self.glow_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.glow_anim.setLoopCount(-1)
        self.glow_anim.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Fundo branco (padrão VTEX)
        painter.fillRect(self.rect(), QColor(255, 255, 255))

        # Linhas diagonais cinza-claro
        painter.setPen(QPen(QColor(200, 200, 200, 30), 1))  # opacidade leve
        spacing = 20
        for i in range(-self.height(), self.width(), spacing):
            painter.drawLine(i, 0, i + self.height(), self.height())

        # Brilho central branco suave
        if self._glow_value > 0:
            center = self.rect().center()
            radius = min(self.width(), self.height()) * 1 * self._glow_value

            radial = QLinearGradient(
                center.x() - radius, center.y() - radius,
                center.x() + radius, center.y() + radius
            )
            radial.setColorAt(0, QColor(self.glow_color.red(), self.glow_color.green(), self.glow_color.blue(), int(100 * self._glow_value)))
            radial.setColorAt(1, QColor(255, 255, 255))


            painter.setBrush(radial)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(center, radius, radius)

    # Propriedades animadas
    def get_glow_value(self):
        return getattr(self, "_glow_value", 0)

    def set_glow_value(self, value):
        self._glow_value = value
        self.update()

    glow_value = Property(float, get_glow_value, set_glow_value)

    # Atualizações de UI
    def set_progress(self, value):
        self.progress.setValue(value)
        self.percentage.setText(f"{value}%")

    def set_message(self, message):
        self.label.setText(message)

    def set_status(self, status):
        self.status.setText(status)