"""
Aba de JSON Completo
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QPushButton
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from config import *


class JsonTab(QWidget):
    """Aba de JSON completo"""
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.json_edit = QTextEdit()
        self.json_edit.setFont(QFont("Consolas", 10))
        self.json_edit.setReadOnly(True)
        self.json_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COR_SECUNDARIA};
                color: {COR_TEXTO};
                border: 1px solid {COR_BORDA};
            }}
        """)
        
        self.copy_btn = QPushButton("Copiar JSON")
        self.copy_btn.setFont(QFont("Arial", 9))
        self.copy_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COR_PRIMARIA};
                color: {COR_SECUNDARIA};
                padding: 5px 10px;
                border-radius: 4px;
            }}
            QPushButton:hover {{
                background-color: #004d00;
            }}
        """)
        self.copy_btn.clicked.connect(self.copiar_json)
        
        layout.addWidget(self.json_edit)
        layout.addWidget(self.copy_btn, 0, Qt.AlignRight)
    
    def copiar_json(self):
        """Copia o JSON para a área de transferência"""
        from PySide6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(self.json_edit.toPlainText())
        self.parent.atualizar_status("JSON copiado para a área de transferência!", "green")

