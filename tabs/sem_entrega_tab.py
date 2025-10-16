"""
Aba de Lojas Sem Entrega
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QScrollArea
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from config import *


class SemEntregaTab(QWidget):
    """Aba de lojas sem entrega"""
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Título da aba
        sem_entrega_title = QLabel("Lojas Sem Entrega Disponível")
        sem_entrega_title.setFont(QFont("Arial", 14, QFont.Bold))
        sem_entrega_title.setStyleSheet(f"color: {COR_PRIMARIA}; padding-bottom: 10px;")
        sem_entrega_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(sem_entrega_title)
        
        # Campo de pesquisa
        pesquisa_layout = QHBoxLayout()
        pesquisa_label = QLabel("Pesquisar loja:")
        pesquisa_label.setFont(QFont("Arial", 10, QFont.Bold))
        pesquisa_label.setStyleSheet(f"color: {COR_PRIMARIA};")
        
        self.pesquisa_sem_entrega = QLineEdit()
        self.pesquisa_sem_entrega.setPlaceholderText("Digite o nome ou código da loja...")
        self.pesquisa_sem_entrega.setFont(QFont("Arial", 10))
        self.pesquisa_sem_entrega.setStyleSheet(f"""
            background-color: {COR_SECUNDARIA};
            border: 1px solid {COR_BORDA};
            border-radius: 4px;
            padding: 8px;
        """)
        self.pesquisa_sem_entrega.textChanged.connect(self.filtrar_lojas_sem_entrega)
        
        pesquisa_layout.addWidget(pesquisa_label)
        pesquisa_layout.addWidget(self.pesquisa_sem_entrega, 1)
        layout.addLayout(pesquisa_layout)
        
        # Área de scroll para as lojas
        self.sem_entrega_scroll = QScrollArea()
        self.sem_entrega_scroll.setWidgetResizable(True)
        self.sem_entrega_scroll.setStyleSheet(f"background-color: {COR_SECUNDARIA};")
        self.sem_entrega_content = QWidget()
        self.sem_entrega_content.setStyleSheet(f"background-color: {COR_SECUNDARIA};")
        self.sem_entrega_layout = QVBoxLayout(self.sem_entrega_content)
        self.sem_entrega_layout.setAlignment(Qt.AlignTop)
        self.sem_entrega_scroll.setWidget(self.sem_entrega_content)
        
        layout.addWidget(self.sem_entrega_scroll, 1)
    
    def popular_aba_sem_entrega(self, lojas_sem_entrega):
        """Popula a aba de lojas sem entrega com as informações das lojas"""
        # Limpar conteúdo anterior
        for i in reversed(range(self.sem_entrega_layout.count())): 
            widget = self.sem_entrega_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        if not lojas_sem_entrega:
            no_data_label = QLabel("Nenhuma loja sem entrega disponível")
            no_data_label.setFont(QFont("Arial", 12))
            no_data_label.setAlignment(Qt.AlignCenter)
            no_data_label.setStyleSheet("color: #7f8c8d;")
            self.sem_entrega_layout.addWidget(no_data_label)
            return
        
        # Armazenar referência para os labels das lojas para filtragem
        self.labels_lojas_sem_entrega = []
        
        for loja, estoque in lojas_sem_entrega:
            nome_loja = self.parent.formatar_nome_loja(loja)
            
            # Lógica de exibição
            if estoque == 0:
                texto = f"{nome_loja} - Estoque Zerado (Estoque: {estoque} unidades)"
                cor = "#e74c3c"  # Vermelho
            else:
                texto = f"{nome_loja} - Fora do range de CEP (Estoque: {estoque} unidades)"
                cor = "#f39c12"  # Laranja
            
            loja_label = QLabel(texto)
            loja_label.setFont(QFont("Arial", 11))
            loja_label.setStyleSheet(f"color: {cor};")
            # Armazenar ID da loja como propriedade do widget
            loja_label.setProperty("loja_id", loja)
            self.sem_entrega_layout.addWidget(loja_label)
            
            # Adicionar à lista de referências
            self.labels_lojas_sem_entrega.append(loja_label)
    
    def filtrar_lojas_sem_entrega(self, texto):
        """Filtra as lojas sem entrega baseado no texto de pesquisa"""
        if not hasattr(self, 'labels_lojas_sem_entrega'):
            return
            
        texto = texto.lower()
        for label in self.labels_lojas_sem_entrega:
            # Obter o texto do label e o ID da loja
            label_text = label.text().lower()
            loja_id = label.property("loja_id")
            
            # Verificar se o texto é "nacional" para mostrar apenas lojas nacionais
            if texto == "nacional":
                # Verificar se é uma loja nacional
                codigo = loja_id[-6:]  # Últimos 6 caracteres
                codigo2 = loja_id[-10:]  # Últimos 10 caracteres
                
                # Verificar se está na lista de lojas nacionais
                is_nacional = (codigo in self.parent.lojas_nacionais or 
                              codigo2 in self.parent.lojas_nacionais or 
                              loja_id in self.parent.lojas_nacionais)
                
                label.setVisible(is_nacional)
            else:
                # Filtro normal por texto
                if texto in label_text or texto in loja_id.lower():
                    label.setVisible(True)
                else:
                    label.setVisible(False)
