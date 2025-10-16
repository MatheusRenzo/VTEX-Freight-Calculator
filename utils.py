"""
Funções utilitárias do VTEX Freight Calculator
"""
import re
from datetime import datetime, timedelta


def validar_cep(cep):
    """Valida formato de CEP"""
    return re.match(r"^\d{5}-\d{3}$", cep) is not None


def formatar_moeda(valor):
    """Formata valor em moeda brasileira"""
    try:
        valor = float(valor) / 100
        return f"R$ {valor:,.2f}".replace(',', 'v').replace('.', ',').replace('v', '.')
    except:
        return f"R$ {valor/100}"


def calcular_prazo_entrega(shipping_estimate):
    """Calcula data de entrega baseada no prazo"""
    try:
        hoje = datetime.now()
        dias = int(re.search(r'\d+', shipping_estimate).group())
        return (hoje + timedelta(days=dias)).strftime("%d/%m/%Y")
    except:
        return shipping_estimate


def parse_prazo_para_dias(prazo_str):
    """Converte a string de prazo para dias numéricos"""
    if not prazo_str:
        return 0
        
    try:
        if 'bd' in prazo_str:  # dias úteis
            return int(prazo_str.replace('bd', ''))
        elif 'd' in prazo_str:  # dias corridos
            return int(prazo_str.replace('d', ''))
        else:
            return int(prazo_str)  # tentar converter diretamente
    except:
        return 0  # valor padrão em caso de erro


def calcular_estoque_total(inventory_data):
    """Calcula o estoque total a partir dos dados de inventory"""
    if not inventory_data or not inventory_data.get('balance'):
        return 0
    total = 0
    for warehouse in inventory_data['balance']:
        total += warehouse.get('totalQuantity', 0)
    return total


def formatar_endereco(address):
    """Formata o endereço de forma legível"""
    if not address:
        return ""
    
    parts = []
    if address.get('street'):
        street = address['street']
        if address.get('number'):
            street += f", {address['number']}"
        parts.append(street)
    
    if address.get('complement'):
        parts.append(address['complement'])
    
    if address.get('neighborhood'):
        parts.append(address['neighborhood'])
    
    if address.get('city') and address.get('state'):
        parts.append(f"{address['city']} - {address['state']}")
    
    if address.get('postalCode'):
        parts.append(f"CEP: {address['postalCode']}")
    
    return "\n".join(parts)


def formatar_nome_loja(loja_id, codigos_filiais):
    """Formata o ID da loja para um nome amigável usando o dicionário"""
    # Extrair código da loja (últimos 6 caracteres)
    codigo = loja_id[-6:]
    # Verificar se o código existe no dicionário
    if codigo in codigos_filiais:
        return codigos_filiais[codigo]
    else:
        # Se não, tentar extrair o código de 10 caracteres?
        codigo2 = loja_id[-10:]
        return f"seller: ({codigo2})"


def determinar_tipo_loja(loja_id, lojas_nacionais):
    """Determina se a loja é Nacional ou Local baseado no dicionário"""
    # Extrair código da loja (últimos 6 caracteres)
    codigo = loja_id[-6:]
    # Se estiver no dicionário de nacionais, retorna "Nacional", senão "Local"
    return lojas_nacionais.get(codigo, "Local")


def loja_tem_qualquer_entrega(simulation_data):
    """Verifica se a loja tem qualquer tipo de entrega (normal ou retirada)"""
    if not simulation_data:
        return False
    if 'logisticsInfo' not in simulation_data or not simulation_data['logisticsInfo']:
        return False
        
    logistics = simulation_data['logisticsInfo'][0]
    if 'slas' not in logistics or not logistics['slas']:
        return False
        
    return True  # Tem pelo menos uma opção de entrega


def loja_tem_entrega_normal(simulation_data):
    """Verifica se a loja tem opções de entrega normais (excluindo retirada)"""
    if not simulation_data:
        return False
    if 'logisticsInfo' not in simulation_data or not simulation_data['logisticsInfo']:
        return False
        
    logistics = simulation_data['logisticsInfo'][0]
    if 'slas' not in logistics or not logistics['slas']:
        return False
        
    # Verifica se existe pelo menos uma entrega normal (não retirada)
    for sla in logistics['slas']:
        if sla.get('deliveryChannel', '').lower() != 'pickup-in-point':
            return True
    return False
