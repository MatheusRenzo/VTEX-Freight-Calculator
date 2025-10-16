"""
Gerenciador de Configurações - Sistema Genérico para VTEX
"""
import json
import os
import sys
from typing import Dict, List, Any, Optional


class ConfigManager:
    """Gerenciador de configurações da empresa com memória persistente"""
    
    def __init__(self, config_file: str = "empresa_config.json"):
        self.config_file = config_file
        self._is_embedded = self._check_if_embedded()
        self.config = self._load_config()
    
    def _check_if_embedded(self) -> bool:
        """Verifica se está rodando dentro do executável PyInstaller"""
        return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    
    def _get_embedded_config(self) -> Dict[str, Any]:
        """Carrega configuração embarcada do executável"""
        try:
            if self._is_embedded:
                # Criar pasta de configuração no sistema
                config_dir = self._get_config_directory()
                saved_config_path = os.path.join(config_dir, 'empresa_config.json')
                
                if os.path.exists(saved_config_path):
                    with open(saved_config_path, 'r', encoding='utf-8') as f:
                        return json.load(f)
                
                # Se não encontrar configurações salvas, usar a configuração embarcada
                # (que foi incluída no executável durante o build)
                try:
                    # Tentar carregar do diretório de recursos do PyInstaller
                    if hasattr(sys, '_MEIPASS'):
                        embedded_path = os.path.join(sys._MEIPASS, 'empresa_config.json')
                        if os.path.exists(embedded_path):
                            with open(embedded_path, 'r', encoding='utf-8') as f:
                                return json.load(f)
                except:
                    pass
            
            # Se não encontrar, usar configuração padrão
            return self._create_default_config()
        except Exception as e:
            print(f"Erro ao carregar configuração embarcada: {e}")
            return self._create_default_config()
    
    def _get_config_directory(self) -> str:
        """Cria e retorna o diretório de configuração do sistema"""
        try:
            import os
            from pathlib import Path
            
            # Criar pasta no diretório do usuário
            user_home = Path.home()
            app_dir = user_home / "VTEX_Freight_Calculator"
            
            # Criar diretório se não existir
            app_dir.mkdir(exist_ok=True)
            
            return str(app_dir)
        except Exception as e:
            print(f"Erro ao criar diretório de configuração: {e}")
            # Fallback para diretório do executável
            return os.path.dirname(sys.executable)
    
    def _load_config(self) -> Dict[str, Any]:
        """Carrega configurações do arquivo JSON ou do executável embarcado"""
        # Se está rodando como executável, usar configuração embarcada
        if self._is_embedded:
            return self._get_embedded_config()
        
        # Se está rodando como script Python, usar arquivo local
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Erro ao carregar configurações: {e}")
                return self._create_default_config()
        else:
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Cria configuração padrão"""
        return {
            "empresa": {
                "nome": "Sua Empresa",
                "conta_principal": "sua-empresa",
                "app_key": "",
                "app_token": "",
                # Removido user_token - não é mais necessário
            },
            "lojas": [],
            "configuracoes": {
                "sku_padrao": "149718",
                "max_skus_recentes": 5,
                "max_workers": 20,
                "timeout_requests": 10
            },
            "cores": {
                "primaria": "#000000",
                "secundaria": "#FFFFFF",
                "destaque": "#000000",
                "fundo": "#F0F0F0",
                "texto": "#333333",
                "borda": "#CCCCCC",
                "destaque2": "#239623"
            }
        }
    
    def save_config(self):
        """Salva configurações de forma persistente"""
        try:
            if self._is_embedded:
                # Salvar na pasta de configuração do sistema
                config_dir = self._get_config_directory()
                config_path = os.path.join(config_dir, 'empresa_config.json')
                
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
                
                print(f"✅ Configurações salvas em: {config_path}")
                print("   (As configurações ficam salvas na pasta do sistema)")
                return True
            else:
                # Se está rodando como script Python, salvar localmente
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, indent=2, ensure_ascii=False)
                return True
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
            return False
    
    def get_config_info(self) -> str:
        """Retorna informações sobre onde as configurações estão salvas"""
        if self._is_embedded:
            config_dir = self._get_config_directory()
            config_path = os.path.join(config_dir, 'empresa_config.json')
            return f"Configurações salvas em: {config_path}"
        else:
            return f"Configurações salvas em: {self.config_file}"
    
    def get_empresa_info(self) -> Dict[str, str]:
        """Retorna informações da empresa"""
        return self.config.get("empresa", {})
    
    def get_lojas(self) -> List[Dict[str, Any]]:
        """Retorna lista de lojas"""
        return self.config.get("lojas", [])
    
    def get_lojas_ids(self) -> List[str]:
        """Retorna apenas os IDs das lojas"""
        return [loja["id"] for loja in self.get_lojas()]
    
    def get_lojas_nacionais(self) -> Dict[str, str]:
        """Retorna dicionário de lojas nacionais"""
        nacionais = {}
        for loja in self.get_lojas():
            if loja.get("nacional", False):
                codigo = loja.get("codigo_filial", "")
                nome = loja.get("nome_filial", "")
                if codigo and nome:
                    nacionais[codigo] = nome
        return nacionais
    
    def get_codigos_filiais(self) -> Dict[str, str]:
        """Retorna dicionário de códigos e filiais"""
        filiais = {}
        for loja in self.get_lojas():
            codigo = loja.get("codigo_filial", "")
            nome = loja.get("nome_filial", "")
            if codigo and nome:
                filiais[codigo] = nome
        return filiais
    
    def get_configuracoes(self) -> Dict[str, Any]:
        """Retorna configurações gerais"""
        return self.config.get("configuracoes", {})
    
    def get_cores(self) -> Dict[str, str]:
        """Retorna configurações de cores com valores padrão"""
        cores = self.config.get("cores", {})
        return {
            # Cores básicas (Minimalista: Branco com rosa apenas em botões)
            'primaria': cores.get('primaria', '#E91E63'),
            'secundaria': cores.get('secundaria', '#FFFFFF'),
            'destaque': cores.get('destaque', '#E91E63'),
            'fundo': cores.get('fundo', '#FFFFFF'),
            'texto': cores.get('texto', '#333333'),
            'borda': cores.get('borda', '#F5F5F5'),
            'destaque2': cores.get('destaque2', '#C2185B'),
            
            # Cores de status
            'sucesso': cores.get('sucesso', '#27ae60'),
            'erro': cores.get('erro', '#e74c3c'),
            'aviso': cores.get('aviso', '#f39c12'),
            'info': cores.get('info', '#3498db'),
            
            # Cores de hover
            'hover_primaria': cores.get('hover_primaria', '#004d00'),
            'hover_destaque': cores.get('hover_destaque', '#239623'),
            'hover_secundaria': cores.get('hover_secundaria', '#f8f9fa'),
            
            # Efeitos visuais
            'sombra': cores.get('sombra', 'rgba(0,0,0,0.1)'),
            'gradiente_inicio': cores.get('gradiente_inicio', '#2bf0e9'),
            'gradiente_fim': cores.get('gradiente_fim', '#00aa00'),
            
            # Cores de botões
            'botao_secundario': cores.get('botao_secundario', '#6c757d'),
            'botao_perigo': cores.get('botao_perigo', '#dc3545'),
            
            # Cores de links
            'link': cores.get('link', '#007bff'),
            'link_hover': cores.get('link_hover', '#0056b3'),
            
            # Cores alternativas
            'fundo_alternativo': cores.get('fundo_alternativo', '#f8f9fa'),
            'borda_alternativa': cores.get('borda_alternativa', '#dee2e6'),
            
            # Cores de texto
            'texto_secundario': cores.get('texto_secundario', '#6c757d'),
            'texto_muted': cores.get('texto_muted', '#868e96')
        }
    
    def add_loja(self, loja_data: Dict[str, Any]) -> bool:
        """Adiciona uma nova loja"""
        try:
            if "lojas" not in self.config:
                self.config["lojas"] = []
            
            # Verificar se já existe
            for loja in self.config["lojas"]:
                if loja.get("id") == loja_data.get("id"):
                    return False  # Já existe
            
            self.config["lojas"].append(loja_data)
            return True
        except Exception as e:
            print(f"Erro ao adicionar loja: {e}")
            return False
    
    def remove_loja(self, loja_id: str) -> bool:
        """Remove uma loja"""
        try:
            if "lojas" in self.config:
                self.config["lojas"] = [
                    loja for loja in self.config["lojas"] 
                    if loja.get("id") != loja_id
                ]
                return True
            return False
        except Exception as e:
            print(f"Erro ao remover loja: {e}")
            return False
    
    def update_loja(self, loja_id: str, loja_data: Dict[str, Any]) -> bool:
        """Atualiza uma loja existente"""
        try:
            if "lojas" in self.config:
                for i, loja in enumerate(self.config["lojas"]):
                    if loja.get("id") == loja_id:
                        self.config["lojas"][i] = loja_data
                        return True
            return False
        except Exception as e:
            print(f"Erro ao atualizar loja: {e}")
            return False
    
    def update_empresa_info(self, empresa_data: Dict[str, str]) -> bool:
        """Atualiza informações da empresa"""
        try:
            self.config["empresa"].update(empresa_data)
            return True
        except Exception as e:
            print(f"Erro ao atualizar empresa: {e}")
            return False
    
    def update_cores(self, cores_data: Dict[str, str]) -> bool:
        """Atualiza configurações de cores"""
        try:
            self.config["cores"].update(cores_data)
            return True
        except Exception as e:
            print(f"Erro ao atualizar cores: {e}")
            return False
    
    def formatar_nome_loja(self, loja_id: str) -> str:
        """Formata o nome da loja baseado na configuração"""
        for loja in self.get_lojas():
            if loja.get("id") == loja_id:
                return loja.get("nome", loja_id)
        return loja_id
    
    def determinar_tipo_loja(self, loja_id: str) -> str:
        """Determina o tipo da loja"""
        for loja in self.get_lojas():
            if loja.get("id") == loja_id:
                return "Nacional" if loja.get("nacional", False) else "Local"
        return "Local"
    
    def get_seller_id(self, loja_id: str) -> str:
        """Retorna o seller ID da loja"""
        for loja in self.get_lojas():
            if loja.get("id") == loja_id:
                return loja.get("seller_id", loja_id)
        return loja_id
    
    def is_loja_principal(self, loja_id: str) -> bool:
        """Verifica se é a loja principal"""
        empresa = self.get_empresa_info()
        return loja_id == empresa.get("conta_principal", "")
