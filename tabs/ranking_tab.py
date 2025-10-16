"""
Aba de Ranking das Lojas
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QSizePolicy, QSplitter, QScrollArea
)
from PySide6.QtGui import QFont, QBrush, QColor
from PySide6.QtCore import Qt
from config import *
from utils import *


class RankingTab(QWidget):
    """Aba de ranking das lojas"""
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.ranking_scroll = QScrollArea()
        self.ranking_scroll.setWidgetResizable(True)
        self.ranking_scroll.setStyleSheet(f"background-color: {COR_SECUNDARIA};")
        self.ranking_content = QWidget()
        self.ranking_content.setStyleSheet(f"background-color: {COR_SECUNDARIA};")
        self.ranking_layout = QVBoxLayout(self.ranking_content)
        self.ranking_layout.setAlignment(Qt.AlignTop)
        self.ranking_scroll.setWidget(self.ranking_content)
        
        layout.addWidget(self.ranking_scroll)
    
    def exibir_ranking(self, resultados):
        """Exibe o ranking das lojas"""
        # Limpar conteúdo anterior
        for i in reversed(range(self.ranking_layout.count())): 
            widget = self.ranking_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        # Título da seção
        title_label = QLabel("RANKING DAS MELHORES LOJAS (APENAS ENTREGAS)")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            padding: 10px; 
            background-color: {COR_PRIMARIA};
            color: {COR_SECUNDARIA};
            border-radius: 5px;
        """)
        self.ranking_layout.addWidget(title_label)
        
        # Criar splitter vertical para tabela e lojas sem entrega
        splitter = QSplitter(Qt.Vertical)
        splitter.setChildrenCollapsible(False)
        
        # Criar tabela de ranking
        table = self._criar_tabela_ranking(resultados)
        
        # Adicionar tabela ao splitter
        splitter.addWidget(table)
        
        # Adicionar o splitter ao layout da aba
        self.ranking_layout.addWidget(splitter, 1)
    
    def _criar_tabela_ranking(self, resultados):
        """Cria a tabela de ranking"""
        table = QTableWidget()
        table.setColumnCount(7)  # Colunas: Posição, Loja, Tipo, Preço, Prazo, Transportadora, Estoque
        table.setHorizontalHeaderLabels(["Posição", "Loja", "Tipo", "Preço Frete", "Prazo", "Transportadora", "Estoque"])
        
        # Configurar cabeçalhos
        header = table.horizontalHeader()
        header.setSectionsMovable(True)
        header.setStretchLastSection(False)
        
        # Configurar todas as colunas
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Posição
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Loja
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Tipo
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Preço
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Prazo
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Transportadora
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Estoque
        
        # Configurar comportamento da tabela
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        table.setMinimumHeight(300)
        
        # Configurar altura padrão das linhas
        table.verticalHeader().setDefaultSectionSize(25)
        table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        
        # Configurações adicionais
        table.setAlternatingRowColors(True)
        table.setShowGrid(True)
        table.setGridStyle(Qt.SolidLine)
        table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COR_SECUNDARIA};
                gridline-color: #ddd;
                font-size: 10pt;
                color: {COR_TEXTO};
                border: 1px solid {COR_BORDA};
                alternate-background-color: #f8f9fa;
            }}
            QHeaderView::section {{
                background-color: {COR_PRIMARIA};
                color: {COR_SECUNDARIA};
                font-weight: bold;
                padding: 5px;
                border: 1px solid #ddd;
            }}
            QHeaderView::section:hover {{
                background-color: #004d00;
            }}
        """)
        
        # Coletar dados para ranking
        ranking_data = self._coletar_dados_ranking(resultados)
        
        # Preencher tabela
        table.setRowCount(len(ranking_data))
        
        for i, item in enumerate(ranking_data):
            # Posição
            posicao_item = QTableWidgetItem(f"{i+1}º")
            posicao_item.setTextAlignment(Qt.AlignCenter)
            
            # Destaque para top 3
            if i < 3:
                posicao_item.setBackground(QBrush(QColor(50, 205, 50, 50)))
            
            # Loja formatada
            nome_loja = self.parent.formatar_nome_loja(item['loja'])
            loja_item = QTableWidgetItem(f"{nome_loja} ({item['loja']})")
            
            # Tipo da loja
            tipo_item = QTableWidgetItem(item['tipo'])
            tipo_item.setTextAlignment(Qt.AlignCenter)
            
            # Preço formatado
            preco_item = QTableWidgetItem(self.parent.formatar_moeda(item['preco']))
            preco_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            # Prazo
            prazo_item = QTableWidgetItem(item['prazo_str'])
            prazo_item.setTextAlignment(Qt.AlignCenter)
            
            # Transportadora
            transp_item = QTableWidgetItem(item['transportadora'])
            
            # Estoque
            estoque_item = QTableWidgetItem(str(item['estoque']))
            estoque_item.setTextAlignment(Qt.AlignCenter)
            
            table.setItem(i, 0, posicao_item)
            table.setItem(i, 1, loja_item)
            table.setItem(i, 2, tipo_item)
            table.setItem(i, 3, preco_item)
            table.setItem(i, 4, prazo_item)
            table.setItem(i, 5, transp_item)
            table.setItem(i, 6, estoque_item)
        
        return table
    
    def _coletar_dados_ranking(self, resultados):
        """Coleta dados para o ranking"""
        ranking_data = []
        
        for loja, data in resultados.items():
            simulation = data.get('simulation', {})
            if loja_tem_entrega_normal(simulation):
                logistics = simulation['logisticsInfo'][0]
                
                # Filtrar apenas SLAS de entrega normal
                slas_entrega = [
                    sla for sla in logistics['slas'] 
                    if sla.get('deliveryChannel', '').lower() != 'pickup-in-point'
                ]
                
                if slas_entrega:
                    melhor_opcao = min(
                        slas_entrega,
                        key=lambda x: x.get('listPrice', float('inf')),
                        default=None
                    )
                    
                    if melhor_opcao:
                        preco = melhor_opcao.get('listPrice', 0)
                        prazo_str = melhor_opcao.get('shippingEstimate', '')
                        prazo_dias = parse_prazo_para_dias(prazo_str)
                        transportadora = melhor_opcao.get('name', '')
                        
                        if 'deliveryIds' in melhor_opcao and melhor_opcao['deliveryIds']:
                            transportadora = melhor_opcao['deliveryIds'][0].get('courierName', transportadora)
                        
                        # Obter estoque total da loja
                        estoque = 0
                        inventory = data.get('inventory', {})
                        if inventory and inventory.get('balance'):
                            for warehouse in inventory['balance']:
                                estoque += warehouse.get('totalQuantity', 0)
                        
                        ranking_data.append({
                            'loja': loja,
                            'tipo': self.parent.determinar_tipo_loja(loja),
                            'preco': preco,
                            'prazo_str': prazo_str,
                            'prazo_dias': prazo_dias,
                            'transportadora': transportadora,
                            'estoque': estoque
                        })
        
        # Ordenar por: 1. prazo (menor primeiro), 2. preço (menor), 3. estoque (maior)
        ranking_data.sort(key=lambda x: (x['prazo_dias'], x['preco'], -x['estoque']))
        
        return ranking_data
