"""
Classes de thread para processamento paralelo
"""
import requests
import concurrent.futures
from PySide6.QtCore import QThread, Signal


class SimulacaoThread(QThread):
    result_signal = Signal(dict)
    error_signal = Signal(str)
    status_signal = Signal(str, str)
    progress_signal = Signal(int, int)
    
    def __init__(self, cep, lojas, sku, app_key, app_token, conta_principal, max_workers=20):
        super().__init__()
        self.cep = cep
        self.lojas = lojas
        self.sku = sku
        self.app_key = app_key
        self.app_token = app_token
        self.conta_principal = conta_principal
        self.max_workers = max_workers
        self.resultados = {}
    
    def run(self):
        try:
            total = len(self.lojas)
            self.status_signal.emit(f"Iniciando simulação para {total} lojas...", "black")
            
            # Usar ThreadPoolExecutor para processamento paralelo
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Criar lista de futures
                future_to_loja = {
                    executor.submit(self.simular_frete, loja): loja
                    for loja in self.lojas
                }
                
                # Processar resultados conforme ficam prontos
                for idx, future in enumerate(concurrent.futures.as_completed(future_to_loja)):
                    loja = future_to_loja[future]
                    try:
                        data = future.result()
                        if data:
                            self.resultados[loja] = data
                    except Exception as e:
                        self.error_signal.emit(f"Erro na loja {loja}: {str(e)}")
                    
                    # Atualizar progresso
                    self.progress_signal.emit(idx + 1, total)
            
            self.result_signal.emit(self.resultados)
        except Exception as e:
            self.error_signal.emit(f"Ocorreu um erro geral: {str(e)}")
    
    def get_shipping_policies(self, loja):
        # Usar conta principal configurada
        conta_principal = self.conta_principal
        if loja == conta_principal:
            url = f"https://{conta_principal}.vtexcommercestable.com.br/api/logistics/pvt/shipping-policies"
        else:
            url = f"https://{loja}.vtexcommercestable.com.br/api/logistics/pvt/shipping-policies"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-VTEX-API-AppKey": self.app_key,
            "X-VTEX-API-AppToken": self.app_token,
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                policies = response.json()
                # Filtrar políticas ativas
                active_policies = {}
                for policy in policies.get('items', []):
                    if policy.get('isActive', False):
                        active_policies[policy['id']] = policy
                return active_policies
            else:
                return {}
        except:
            return {}
    
    def get_inventory(self, loja, seller, sku):
        # Usar conta principal configurada
        conta_principal = self.conta_principal
        if loja == conta_principal:
            url = f"https://{conta_principal}.vtexcommercestable.com.br/api/logistics/pvt/inventory/skus/{sku}"
        else:
            url = f"https://{loja}.vtexcommercestable.com.br/api/logistics/pvt/inventory/skus/{sku}"
        
        params = {'sellerId': seller}
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-VTEX-API-AppKey": self.app_key,
            "X-VTEX-API-AppToken": self.app_token,
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except:
            return None
    
    def simular_frete(self, loja):
        # Determinar seller baseado na loja
        conta_principal = self.conta_principal
        seller = "1" if loja == conta_principal else loja
        
        # 1. Obter políticas de envio ativas
        active_policies = self.get_shipping_policies(loja)
        
        # 2. Simular a ordem
        if loja == conta_principal:
            url = f"https://{conta_principal}.vtexcommercestable.com.br/api/checkout/pub/orderForms/simulation"
        else:
            url = f"https://{loja}.vtexcommercestable.com.br/api/checkout/pub/orderForms/simulation"
        
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "items": [
                {
                    "id": self.sku,
                    "quantity": 1,
                    "seller": seller
                }
            ],
            "postalCode": self.cep.replace('-', ''),
            "country": "BRA"
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                simulation_data = response.json()
                
                # 3. Filtrar SLAs: apenas as que pertencem às políticas ativas
                if 'logisticsInfo' in simulation_data and simulation_data['logisticsInfo']:
                    for logistics in simulation_data['logisticsInfo']:
                        filtered_slas = []
                        for sla in logistics.get('slas', []):
                            # Verificar cada deliveryId na SLA
                            include_sla = False
                            for delivery in sla.get('deliveryIds', []):
                                courier_id = delivery.get('courierId')
                                if courier_id in active_policies:
                                    include_sla = True
                                    break
                            if include_sla:
                                filtered_slas.append(sla)
                        logistics['slas'] = filtered_slas
                
                # 4. Obter estoque
                inventory_data = self.get_inventory(loja, seller, self.sku)
                
                # Retornar dados completos
                return {
                    "simulation": simulation_data,
                    "active_policies": active_policies,
                    "inventory": inventory_data
                }
            else:
                # Retornar estrutura de erro
                return {
                    "simulation": None,
                    "active_policies": active_policies,
                    "inventory": None,
                    "error": f"Erro na API: Status {response.status_code}"
                }
        except Exception as e:
            return {
                "simulation": None,
                "active_policies": active_policies,
                "inventory": None,
                "error": f"Erro de conexão: {str(e)}"
            }


class EstoqueThread(QThread):
    result_signal = Signal(dict)
    error_signal = Signal(str)
    status_signal = Signal(str, str)
    progress_signal = Signal(int, int)
    
    def __init__(self, sku, lojas, app_key, app_token, conta_principal, max_workers=20):
        super().__init__()
        self.sku = sku
        self.lojas = lojas
        self.app_key = app_key
        self.app_token = app_token
        self.conta_principal = conta_principal
        self.max_workers = max_workers
        self.resultados = {}
    
    def run(self):
        try:
            total = len(self.lojas)
            self.status_signal.emit(f"Iniciando consulta de estoque para {total} lojas...", "black")
            
            # Usar ThreadPoolExecutor para processamento paralelo
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Criar lista de futures
                future_to_loja = {
                    executor.submit(self.get_inventory_for_loja, loja): loja
                    for loja in self.lojas
                }
                
                # Processar resultados conforme ficam prontos
                for idx, future in enumerate(concurrent.futures.as_completed(future_to_loja)):
                    loja = future_to_loja[future]
                    try:
                        result = future.result()
                        if result:
                            self.resultados[result['loja']] = result['estoque_data']
                    except Exception as e:
                        self.error_signal.emit(f"Erro na loja {loja}: {str(e)}")
                    
                    # Atualizar progresso
                    self.progress_signal.emit(idx + 1, total)
            
            self.result_signal.emit(self.resultados)
        except Exception as e:
            self.error_signal.emit(f"Erro geral: {str(e)}")
    
    def get_inventory_for_loja(self, loja):
        conta_principal = self.conta_principal
        seller = "1" if loja == conta_principal else loja
        inventory_data = self.get_inventory(loja, seller, self.sku)
        estoque_data = {'total': 0, 'principal': 0}
        
        if inventory_data:
            total_estoque = 0
            estoque_principal = 0
            for warehouse in inventory_data.get('balance', []):
                quantidade = warehouse.get('totalQuantity', 0)
                total_estoque += quantidade
                if warehouse.get('warehouseId') == '1_1':
                    estoque_principal = quantidade
            
            estoque_data = {
                'total': total_estoque,
                'principal': estoque_principal
            }
        
        return {'loja': loja, 'estoque_data': estoque_data}
    
    def get_inventory(self, loja, seller, sku):
        # Usar conta principal configurada
        conta_principal = self.conta_principal
        if loja == conta_principal:
            url = f"https://{conta_principal}.vtexcommercestable.com.br/api/logistics/pvt/inventory/skus/{sku}"
        else:
            url = f"https://{loja}.vtexcommercestable.com.br/api/logistics/pvt/inventory/skus/{sku}"
        
        params = {'sellerId': seller}
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-VTEX-API-AppKey": self.app_key,
            "X-VTEX-API-AppToken": self.app_token,
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except:
            return None
