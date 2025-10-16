"""
Aba de Resumo Detalhado
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QGroupBox, QScrollArea, QFrame
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from config import *
from utils import *


class ResumoTab(QWidget):
    """Aba de resumo detalhado"""
    
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Adicionar combobox para seleção de loja
        self.loja_selector_layout = QHBoxLayout()
        self.loja_selector_label = QLabel("Selecionar Loja:")
        self.loja_selector_label.setFont(QFont("Arial", 10))
        self.loja_selector = QComboBox()
        self.loja_selector.setFont(QFont("Arial", 10))
        self.loja_selector.setMinimumWidth(250)
        self.loja_selector.currentIndexChanged.connect(self.parent.atualizar_resumo)
        
        self.loja_selector_layout.addWidget(self.loja_selector_label)
        self.loja_selector_layout.addWidget(self.loja_selector)
        self.loja_selector_layout.addStretch()
        
        layout.addLayout(self.loja_selector_layout)
        
        self.resumo_scroll = QScrollArea()
        self.resumo_scroll.setWidgetResizable(True)
        self.resumo_scroll.setStyleSheet(f"background-color: {COR_SECUNDARIA};")
        self.resumo_content = QWidget()
        self.resumo_content.setStyleSheet(f"background-color: {COR_SECUNDARIA};")
        self.resumo_layout = QVBoxLayout(self.resumo_content)
        self.resumo_layout.setAlignment(Qt.AlignTop)
        self.resumo_scroll.setWidget(self.resumo_content)
        
        layout.addWidget(self.resumo_scroll, 1)
    
    def exibir_resumo_para_loja(self, loja, data):
        """Exibe resumo detalhado para uma loja específica"""
        # Título da seção
        nome_formatado = self.parent.formatar_nome_loja(loja)
        title_label = QLabel(f"DETALHES DA LOJA: {nome_formatado.upper()} ({loja})")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            padding: 10px; 
            background-color: {COR_PRIMARIA};
            color: {COR_SECUNDARIA};
            border-radius: 5px;
        """)
        self.resumo_layout.addWidget(title_label)
        
        simulation = data.get('simulation', {})
        if not loja_tem_qualquer_entrega(simulation):
            no_data_label = QLabel("Nenhuma opção de entrega disponível para esta loja")
            no_data_label.setFont(QFont("Arial", 12))
            no_data_label.setAlignment(Qt.AlignCenter)
            no_data_label.setStyleSheet("color: #e74c3c;")
            self.resumo_layout.addWidget(no_data_label)
            return
            
        if 'logisticsInfo' in simulation and simulation['logisticsInfo']:
            logistics = simulation['logisticsInfo'][0]
            logistics_group = QGroupBox(f"LOJA: {nome_formatado.upper()} ({loja})")
            logistics_group.setFont(QFont("Arial", 10, QFont.Bold))
            logistics_group.setStyleSheet(f"""
                QGroupBox {{
                    background-color: {COR_SECUNDARIA};
                    border: 1px solid {COR_BORDA};
                    border-radius: 5px;
                    margin-top: 10px;
                }}
            """)
            logistics_layout = QVBoxLayout(logistics_group)
            
            # Separar SLAs em normais e retirada
            slas_normais = []
            slas_retirada = []
            for sla in logistics.get('slas', []):
                if sla.get('deliveryChannel', '').lower() == 'pickup-in-point':
                    slas_retirada.append(sla)
                else:
                    slas_normais.append(sla)
            
            # Exibir entregas normais
            if slas_normais:
                normais_group = QGroupBox("ENTREGAS")
                normais_group.setFont(QFont("Arial", 9, QFont.Bold))
                normais_layout = QVBoxLayout(normais_group)
                
                for i, sla in enumerate(slas_normais):
                    sla_group = QGroupBox(f"OPÇÃO {i+1}: {sla.get('name', '').upper()}")
                    sla_group.setFont(QFont("Arial", 9, QFont.Bold))
                    sla_layout = QVBoxLayout(sla_group)
                    
                    # Informações principais
                    price_layout = QHBoxLayout()
                    price = self.parent.formatar_moeda(sla.get('listPrice', 0))
                    price_label = QLabel(price)
                    price_label.setFont(QFont("Arial", 14, QFont.Bold))
                    price_label.setStyleSheet("color: #27ae60;")
                    price_layout.addWidget(price_label)
                    
                    # Detalhes da entrega
                    delivery_layout = QVBoxLayout()
                    
                    prazo = sla.get('shippingEstimate', '')
                    data_estimada = self.parent.calcular_prazo_entrega(prazo)
                    
                    prazo_label = QLabel(f"Prazo: {prazo}")
                    prazo_label.setFont(QFont("Arial", 10, QFont.Bold))
                    delivery_layout.addWidget(prazo_label)
                    
                    data_label = QLabel(f"Previsão: {data_estimada}")
                    data_label.setFont(QFont("Arial", 10))
                    delivery_layout.addWidget(data_label)
                    
                    transit_label = QLabel(f"Trânsito: {sla.get('transitTime', '')} dias")
                    transit_label.setFont(QFont("Arial", 9))
                    delivery_layout.addWidget(transit_label)
                    
                    price_layout.addLayout(delivery_layout)
                    sla_layout.addLayout(price_layout)
                    
                    # Transportadoras
                    if 'deliveryIds' in sla and sla['deliveryIds']:
                        couriers_group = QGroupBox("TRANSPORTADORAS")
                        couriers_group.setFont(QFont("Arial", 9, QFont.Bold))
                        couriers_layout = QVBoxLayout(couriers_group)
                        
                        for delivery in sla['deliveryIds']:
                            courier_text = f"• {delivery.get('courierId', '')} "
                            courier_text += f"(Modalidade: {delivery.get('courierName', '')})"
                            courier_label = QLabel(courier_text)
                            courier_label.setFont(QFont("Arial", 12))
                            couriers_layout.addWidget(courier_label)
                        
                        sla_layout.addWidget(couriers_group)
                    
                    normais_layout.addWidget(sla_group)
                
                logistics_layout.addWidget(normais_group)
            
            # Exibir pontos de retirada
            if slas_retirada:
                retirada_group = QGroupBox("PONTOS DE RETIRADA")
                retirada_group.setFont(QFont("Arial", 9, QFont.Bold))
                retirada_layout = QVBoxLayout(retirada_group)
                
                for i, sla in enumerate(slas_retirada):
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
                        if 'complement' in address and address['complement']:
                            endereco_text += f" - {address['complement']}"
                    
                    # Disponibilidade
                    disponivel = "Disponível para retirada" if pickup_info.get('isDisposable', True) else "disponivel"
            
                    # Criar frame com informações
                    pickup_frame = QFrame()
                    pickup_frame.setFrameShape(QFrame.StyledPanel)
                    pickup_frame.setStyleSheet(f"""
                        QFrame {{
                            background-color: {COR_SECUNDARIA};
                            border: 1px solid {COR_BORDA};
                            border-radius: 5px;
                            padding: 10px;
                        }}
                    """)
                    pickup_layout = QVBoxLayout(pickup_frame)
                    
                    # Nome do ponto
                    name_label = QLabel(f"<b>{ponto_nome}</b>")
                    name_label.setFont(QFont("Arial", 10, QFont.Bold))
                    name_label.setStyleSheet("color: #228B22;")
                    pickup_layout.addWidget(name_label)
                    
                    # Preço
                    price_label = QLabel(f"<b>Preço:</b> {preco}")
                    price_label.setFont(QFont("Arial", 10))
                    pickup_layout.addWidget(price_label)
                    
                    # Informações em linha
                    info_layout = QHBoxLayout()
                    
                    # Prazo de retirada
                    prazo_label = QLabel(f"<b>Prazo:</b> {prazo}")
                    prazo_label.setFont(QFont("Arial", 9))
                    info_layout.addWidget(prazo_label)
                    
                    # Distância
                    distancia_label = QLabel(f"<b>Distância:</b> {distancia_text}")
                    distancia_label.setFont(QFont("Arial", 9))
                    info_layout.addWidget(distancia_label)
                    
                    # Disponibilidade
                    disp_label = QLabel(f"<b>Status:</b> {disponivel}")
                    disp_label.setFont(QFont("Arial", 9))
                    info_layout.addWidget(disp_label)
                    
                    info_layout.addStretch()
                    pickup_layout.addLayout(info_layout)
                    
                    # Endereço
                    if endereco_text:
                        endereco_label = QLabel(f"<b>Endereço:</b> {endereco_text}")
                        endereco_label.setFont(QFont("Arial", 9))
                        endereco_label.setStyleSheet("color: #7f8c8d;")
                        pickup_layout.addWidget(endereco_label)
                    
                    # Adicionar ao grupo de retirada
                    retirada_layout.addWidget(pickup_frame)
                
                logistics_layout.addWidget(retirada_group)
            
            # Exibir estoque
            inventory = data.get('inventory')
            if inventory:
                estoque_group = QGroupBox("ESTOQUE DISPONÍVEL")
                estoque_group.setFont(QFont("Arial", 9, QFont.Bold))
                estoque_layout = QVBoxLayout(estoque_group)
                
                # Calcular total
                total_balance = self.parent.calcular_estoque_total(inventory)
                total_label = QLabel(f"Total: {total_balance} unidades")
                total_label.setFont(QFont("Arial", 10, QFont.Bold))
                estoque_layout.addWidget(total_label)
                
                # Listar armazéns com estoque
                if inventory.get('balance'):
                    for warehouse in inventory['balance']:
                        if warehouse.get('totalQuantity',0) > 0:
                            wh_text = f"{warehouse.get('warehouseId', '')}: {warehouse.get('totalQuantity')} unidades"
                            wh_label = QLabel(wh_text)
                            wh_label.setFont(QFont("Arial", 9))
                            estoque_layout.addWidget(wh_label)
                
                logistics_layout.addWidget(estoque_group)
            
            self.resumo_layout.addWidget(logistics_group)
