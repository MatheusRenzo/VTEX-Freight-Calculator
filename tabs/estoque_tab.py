"""
Aba de Consulta de Estoque
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
)
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt
from config import *


class EstoqueTab(QWidget):
    """Aba de consulta de estoque"""
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Título e campo de entrada para estoque
        estoque_title = QLabel("Consulta de Estoque")
        estoque_title.setFont(QFont("Arial", 14, QFont.Bold))
        estoque_title.setStyleSheet(f"color: {COR_PRIMARIA}; padding-bottom: 10px;")
        estoque_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(estoque_title)
        
        # Layout de entrada
        estoque_input_layout = QHBoxLayout()
        estoque_sku_label = QLabel("SKU:")
        estoque_sku_label.setFont(QFont("Arial", 10, QFont.Bold))
        estoque_sku_label.setStyleSheet(f"color: {COR_PRIMARIA};")
        
        self.estoque_sku_input = QComboBox()
        self.estoque_sku_input.setEditable(True)
        self.estoque_sku_input.setFont(QFont("Arial", 10))
        self.estoque_sku_input.setStyleSheet(f"""
            background-color: {COR_SECUNDARIA};
            border: 1px solid {COR_BORDA};
            border-radius: 4px;
            padding: 5px;
        """)
        self.estoque_sku_input.addItems(self.parent.skus_recentes)
        self.estoque_sku_input.setCurrentText(SKU_DEFAULT)
        
        self.consultar_estoque_btn = QPushButton("CONSULTAR ESTOQUE")
        self.consultar_estoque_btn.setFont(QFont("Arial", 10, QFont.Bold))
        self.consultar_estoque_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COR_DESTAQUE2};
                color: {COR_SECUNDARIA};
                padding: 8px 15px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: #239623;
            }}
            QPushButton:disabled {{
                background-color: #a0a0a0;
            }}
        """)
        self.consultar_estoque_btn.clicked.connect(self.parent.iniciar_consulta_estoque)
        
        estoque_input_layout.addWidget(estoque_sku_label)
        estoque_input_layout.addWidget(self.estoque_sku_input, 1)
        estoque_input_layout.addWidget(self.consultar_estoque_btn)
        layout.addLayout(estoque_input_layout)
        
        # Tabela de estoque
        self.estoque_table = QTableWidget()
        self.estoque_table.setColumnCount(3)
        self.estoque_table.setHorizontalHeaderLabels(["Loja", "Estoque Total", "Estoque Principal (1_1)"])
        self.estoque_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.estoque_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.estoque_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.estoque_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.estoque_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.estoque_table.setSortingEnabled(True)
        self.estoque_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COR_SECUNDARIA};
                gridline-color: #ddd;
                font-size: 10pt;
                color: {COR_TEXTO};
                border: 1px solid {COR_BORDA};
                border-radius: 4px;
            }}
            QHeaderView::section {{
                background-color: {COR_PRIMARIA};
                color: {COR_SECUNDARIA};
                font-weight: bold;
                padding: 5px;
                border: none;
            }}
        """)
        layout.addWidget(self.estoque_table, 1)
    
    def mostrar_resultados_estoque(self, resultados):
        """Exibe resultados da consulta de estoque"""
        self.consultar_estoque_btn.setEnabled(True)
        self.consultar_estoque_btn.setText("CONSULTAR ESTOQUE")
        
        self.estoque_table.setRowCount(len(resultados))
        self.estoque_table.setSortingEnabled(False)  # Desabilitar ordenação durante atualização
        
        row = 0
        for loja, estoque_data in resultados.items():
            nome_loja = self.parent.formatar_nome_loja(loja)
            total = estoque_data.get('total', 0)
            principal = estoque_data.get('principal', 0)
            
            loja_item = QTableWidgetItem(nome_loja)
            total_item = QTableWidgetItem(str(total))
            principal_item = QTableWidgetItem(str(principal))
            
            # Destacar estoque zerado
            if total == 0:
                loja_item.setBackground(QColor(255, 200, 200))  # Vermelho claro
                total_item.setBackground(QColor(255, 200, 200))
                principal_item.setBackground(QColor(255, 200, 200))
            # Destacar estoque baixo
            elif total <= 5:
                loja_item.setBackground(QColor(255, 255, 200))  # Amarelo claro
                total_item.setBackground(QColor(255, 255, 200))
                principal_item.setBackground(QColor(255, 255, 200))
            
            self.estoque_table.setItem(row, 0, loja_item)
            self.estoque_table.setItem(row, 1, total_item)
            self.estoque_table.setItem(row, 2, principal_item)
            
            row += 1
        
        self.estoque_table.setSortingEnabled(True)  # Reabilitar ordenação
        self.parent.atualizar_status(f"Consulta de estoque concluída! {len(resultados)} lojas processadas.", "green")

