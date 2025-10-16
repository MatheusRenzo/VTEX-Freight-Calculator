"""
Componentes de interface do VTEX Freight Calculator
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, 
    QPushButton, QFrame, QGroupBox, QListWidget, QListWidgetItem,
    QSplitter, QStatusBar
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
# As cores serão passadas como parâmetros


class InputPanel(QWidget):
    """Painel de entrada de dados"""
    
    def __init__(self, parent, cores):
        super().__init__()
        self.parent = parent
        self.cores = cores
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Grupo de entrada de dados
        input_group = QGroupBox("Dados para Simulação")
        input_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                font-size: 12pt;
                color: {self.cores['texto']};
                border: 1px solid {self.cores['borda']};
                border-radius: 5px;
                margin-top: 1ex;
                background-color: {self.cores['secundaria']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                background-color: {self.cores['secundaria']};
            }}
        """)
        layout.addWidget(input_group)
        
        input_layout = QVBoxLayout(input_group)
        input_layout.setSpacing(10)
        
        # Campo CEP
        cep_layout = QHBoxLayout()
        cep_label = QLabel("CEP:")
        cep_label.setFont(QFont("Arial", 10))
        self.cep_input = QLineEdit("05372-110")
        self.cep_input.setFont(QFont("Arial", 10))
        self.cep_input.setStyleSheet(f"background-color: {self.cores['secundaria']};")
        cep_layout.addWidget(cep_label)
        cep_layout.addWidget(self.cep_input, 1)
        input_layout.addLayout(cep_layout)
        
        # Campo SKU
        sku_layout = QHBoxLayout()
        sku_label = QLabel("SKU:")
        sku_label.setFont(QFont("Arial", 10))
        
        self.sku_combo = QComboBox()
        self.sku_combo.setEditable(True)
        self.sku_combo.setFont(QFont("Arial", 10))
        self.sku_combo.setStyleSheet(f"background-color: {self.cores['secundaria']};")
        self.sku_combo.addItems(self.parent.skus_recentes)
        self.sku_combo.setCurrentText(self.parent.sku_default)
        
        sku_layout.addWidget(sku_label)
        sku_layout.addWidget(self.sku_combo, 1)
        input_layout.addLayout(sku_layout)

        # Grupo de seleção de lojas
        loja_group = QGroupBox("Lojas para Comparação")
        loja_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                font-size: 10pt;
                color: {self.cores['texto']};
                border: 1px solid {self.cores['borda']};
                border-radius: 5px;
                margin-top: 1ex;
                background-color: {self.cores['secundaria']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
                background-color: {self.cores['secundaria']};
            }}
        """)
        loja_layout = QVBoxLayout(loja_group)
        
        # Filtro para lojas
        filter_layout = QHBoxLayout()
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Filtrar lojas...")
        self.filter_input.setStyleSheet(f"background-color: {self.cores['secundaria']};")
        self.filter_input.textChanged.connect(self.parent.filtrar_lojas)
        filter_layout.addWidget(self.filter_input)
        
        # Botões de seleção
        btn_layout = QHBoxLayout()
        self.select_all_btn = QPushButton("Selecionar Todas")
        self.select_all_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.cores['borda']};
                color: {self.cores['texto']};
                padding: 5px;
                border-radius: 4px;
                border: 1px solid {self.cores['borda']};
            }}
            QPushButton:hover {{
                background-color: {self.cores['fundo']};
            }}
        """)
        self.select_all_btn.clicked.connect(self.parent.selecionar_todas)
        
        self.deselect_all_btn = QPushButton("Desselecionar Todas")
        self.deselect_all_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.cores['borda']};
                color: {self.cores['texto']};
                padding: 5px;
                border-radius: 4px;
                border: 1px solid {self.cores['borda']};
            }}
            QPushButton:hover {{
                background-color: {self.cores['fundo']};
            }}
        """)
        self.deselect_all_btn.clicked.connect(self.parent.desselecionar_todas)
        
        btn_layout.addWidget(self.select_all_btn)
        btn_layout.addWidget(self.deselect_all_btn)
        
        loja_layout.addLayout(filter_layout)
        loja_layout.addLayout(btn_layout)
        
        # Lista de lojas
        self.lojas_list = QListWidget()
        self.lojas_list.setStyleSheet(f"""
            QListWidget {{
                background-color: {self.cores['secundaria']};
                border: 1px solid {self.cores['borda']};
                border-radius: 4px;
            }}
        """)
        self.lojas_list.setSelectionMode(QListWidget.MultiSelection)
        loja_layout.addWidget(self.lojas_list, 1)
        
        input_layout.addWidget(loja_group, 1)
        
        # Botões
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        self.simular_btn = QPushButton("▶ SIMULAR FRETE")
        self.simular_btn.setFont(QFont("Arial", 10, QFont.Bold))
        self.simular_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.cores['destaque']};
                color: {self.cores['secundaria']};
                padding: 10px 20px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {self.cores['destaque2']};
            }}
            QPushButton:disabled {{
                background-color: #a0a0a0;
            }}
        """)
        self.simular_btn.clicked.connect(self.parent.iniciar_simulacao_thread)
        
        self.limpar_btn = QPushButton("LIMPAR")
        self.limpar_btn.setFont(QFont("Arial", 10))
        self.limpar_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.cores['borda']};
                color: {self.cores['texto']};
                padding: 10px 20px;
                border-radius: 5px;
                border: 1px solid {self.cores['borda']};
            }}
            QPushButton:hover {{
                background-color: {self.cores['fundo']};
            }}
        """)
        self.limpar_btn.clicked.connect(self.parent.limpar_resultados)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.simular_btn)
        buttons_layout.addWidget(self.limpar_btn)
        
        input_layout.addLayout(buttons_layout)
    
    def aplicar_cores_dinamicamente(self, cores):
        """Aplica cores dinamicamente aos componentes"""
        self.cores = cores
        
        # Aplicar cores aos botões
        self.simular_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {cores['destaque']};
                color: {cores['secundaria']};
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {cores.get('destaque2', '#C2185B')};
            }}
        """)
        
        self.limpar_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {cores['borda']};
                color: {cores['texto']};
                border: 1px solid {cores['borda']};
                padding: 10px 20px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {cores.get('destaque2', '#C2185B')};
            }}
        """)
        
        # Aplicar cores aos inputs
        input_style = f"""
            QLineEdit, QComboBox {{
                background-color: {cores['secundaria']};
                color: {cores['texto']};
                border: 1px solid {cores['borda']};
                padding: 8px;
                border-radius: 4px;
            }}
            QLineEdit:focus, QComboBox:focus {{
                border-color: {cores['destaque']};
            }}
        """
        
        self.cep_input.setStyleSheet(input_style)
        self.filter_input.setStyleSheet(input_style)
        self.sku_combo.setStyleSheet(input_style)
        self.lojas_list.setStyleSheet(input_style)
    


class HeaderWidget(QLabel):
    """Cabeçalho da aplicação"""
    
    def __init__(self, cores, empresa_nome="Sua Empresa"):
        super().__init__(f"{empresa_nome} - VTEX Freight Calculator")
        self.cores = cores
        self.init_ui()
    
    def init_ui(self):
        header_font = QFont("Arial", 16, QFont.Bold)
        self.setFont(header_font)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(f"""
            background-color: {self.cores['fundo']};
            color: {self.cores['texto']};
            padding: 15px;
            border-radius: 8px;
            border: 1px solid {self.cores['borda']};
        """)


class StatusBarWidget(QStatusBar):
    """Barra de status personalizada"""
    
    def __init__(self, cores):
        super().__init__()
        self.cores = cores
        self.init_ui()
    
    def init_ui(self):
        self.setFont(QFont("Arial", 9))
        self.setStyleSheet(f"background-color: {self.cores['secundaria']}; color: {self.cores['texto']};")
        self.showMessage("Pronto para simular")
