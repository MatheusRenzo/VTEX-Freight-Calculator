"""
Aba de Pontos de Retirada
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QSizePolicy, QFrame, QGroupBox, QScrollArea
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from config import *
from utils import *


class RetiradaTab(QWidget):
    """Aba de pontos de retirada"""
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.retirada_scroll = QScrollArea()
        self.retirada_scroll.setWidgetResizable(True)
        self.retirada_scroll.setStyleSheet(f"background-color: {COR_SECUNDARIA};")
        self.retirada_content = QWidget()
        self.retirada_content.setStyleSheet(f"background-color: {COR_SECUNDARIA};")
        self.retirada_layout = QVBoxLayout(self.retirada_content)
        self.retirada_layout.setAlignment(Qt.AlignTop)
        self.retirada_scroll.setWidget(self.retirada_content)
        
        layout.addWidget(self.retirada_scroll)
    
    def exibir_pontos_retirada(self, resultados):
        """Exibe pontos de retirada"""
        # Limpar conteúdo anterior
        for i in reversed(range(self.retirada_layout.count())): 
            widget = self.retirada_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        # Título da seção
        title_label = QLabel("PONTOS DE RETIRADA")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            padding: 10px; 
            background-color: {COR_PRIMARIA};
            color: {COR_SECUNDARIA};
            border-radius: 5px;
        """)
        self.retirada_layout.addWidget(title_label)
        
        # Container principal com scroll
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setAlignment(Qt.AlignTop)
        
        # Processar resultados por loja
        for loja, data in resultados.items():
            simulation = data.get('simulation', {})
            if not loja_tem_qualquer_entrega(simulation):
                continue
                
            if 'logisticsInfo' in simulation and simulation['logisticsInfo']:
                logistics = simulation['logisticsInfo'][0]
                if 'slas' not in logistics or not logistics['slas']:
                    continue
                    
                # Verificar se há pontos de retirada nesta loja
                pontos_retirada = []
                for sla in logistics.get('slas', []):
                    if sla.get('deliveryChannel', '').lower() == 'pickup-in-point':
                        pontos_retirada.append(sla)
                
                if not pontos_retirada:
                    continue
                    
                # Grupo para a loja
                nome_loja = self.parent.formatar_nome_loja(loja)
                loja_group = QGroupBox(f"LOJA: {nome_loja.upper()} ({loja})")
                loja_group.setFont(QFont("Arial", 10, QFont.Bold))
                loja_group.setStyleSheet(f"""
                    QGroupBox {{
                        background-color: {COR_SECUNDARIA};
                        border: 1px solid {COR_BORDA};
                        border-radius: 5px;
                        margin-top: 10px;
                    }}
                """)
                loja_layout = QVBoxLayout(loja_group)
                loja_layout.setSpacing(10)
                
                # Tabela para pontos de retirada
                table = self._criar_tabela_retirada(pontos_retirada)
                loja_layout.addWidget(table)
                container_layout.addWidget(loja_group)
        
        # Se não houver pontos de retirada
        if container_layout.count() == 0:
            no_data_label = QLabel("Nenhum ponto de retirada disponível")
            no_data_label.setFont(QFont("Arial", 12))
            no_data_label.setAlignment(Qt.AlignCenter)
            no_data_label.setStyleSheet("color: #7f8c8d;")
            container_layout.addWidget(no_data_label)
        
        # Adicionar ao layout da aba
        self.retirada_layout.addWidget(container)
    
    def _criar_tabela_retirada(self, pontos_retirada):
        """Cria tabela de pontos de retirada"""
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Ponto", "Prazo", "Distância", "Preço", "Endereço"])
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.setMinimumHeight(200)
        table.verticalHeader().setVisible(False)
        
        # Ajuste individual das colunas
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Ponto
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Prazo
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Distância
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Preço
        header.setSectionResizeMode(4, QHeaderView.Stretch)           # Endereço
        
        # Estilo visual da tabela
        table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COR_SECUNDARIA};
                gridline-color: #ddd;
                font-size: 9pt;
                color: {COR_TEXTO};
                border: 1px solid {COR_BORDA};
            }}
            QHeaderView::section {{
                background-color: {COR_PRIMARIA};
                color: {COR_SECUNDARIA};
                font-weight: bold;
                padding: 4px;
            }}
        """)
        
        table.setRowCount(len(pontos_retirada))
        
        for i, sla in enumerate(pontos_retirada):
            # Obter informações do ponto de retirada
            pickup_info = sla.get('pickupStoreInfo', {})
            address = pickup_info.get('address', {})
            
            # Nome do ponto
            ponto_nome = pickup_info.get('friendlyName', sla.get('name', 'Ponto de Retirada'))
            
            # Prazo
            prazo = sla.get('shippingEstimate', '')
            
            # Distância
            distancia = sla.get('pickupDistance', 0)
            distancia_text = f"{distancia:.1f} km" if distancia else "-"
            
            # Preço
            preco = self.parent.formatar_moeda(sla.get('price', 0))
            
            # Endereço
            endereco_text = ""
            if 'street' in address:
                endereco_text += address['street']
                if 'number' in address:
                    endereco_text += f", {address['number']}"
            
            # Preencher a tabela
            name_item = QTableWidgetItem(ponto_nome)
            name_item.setToolTip(ponto_nome)
            
            prazo_item = QTableWidgetItem(prazo)
            
            distancia_item = QTableWidgetItem(distancia_text)
            distancia_item.setTextAlignment(Qt.AlignCenter)
            
            preco_item = QTableWidgetItem(preco)
            preco_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            endereco_item = QTableWidgetItem(endereco_text)
            endereco_item.setToolTip(endereco_text)

            table.setItem(i, 0, name_item)
            table.setItem(i, 1, prazo_item)
            table.setItem(i, 2, distancia_item)
            table.setItem(i, 3, preco_item)
            table.setItem(i, 4, endereco_item)
        
        return table
