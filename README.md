# 🚚 VTEX Freight Calculator

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.0+-green.svg)
![VTEX](https://img.shields.io/badge/VTEX-API-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

> **Simulador de Frete VTEX** - Aplicação desktop para simular custos de frete e consultar estoque em múltiplas lojas VTEX simultaneamente com interface moderna e processamento paralelo.

## 📋 Índice

- [🎯 Sobre o Projeto](#-sobre-o-projeto)
- [✨ Funcionalidades](#-funcionalidades)
- [🖥️ Interface](#️-interface)
- [📦 Instalação](#-instalação)
- [🚀 Como Usar](#-como-usar)
- [⚙️ Configuração](#️-configuração)
- [🔧 Gerando o Executável](#-gerando-o-executável)
- [📋 Requisitos](#-requisitos)
- [🏗️ Arquitetura](#️-arquitetura)
- [🤝 Contribuição](#-contribuição)
- [📄 Licença](#-licença)

## 🎯 Sobre o Projeto

O **VTEX Freight Calculator** é uma aplicação desktop desenvolvida em Python com PySide6 que permite simular custos de frete e consultar estoque em múltiplas lojas VTEX simultaneamente. A aplicação utiliza processamento paralelo com threads para otimizar as consultas à API VTEX e oferece uma interface moderna e intuitiva para análise de dados de logística.

### 🎨 Características Técnicas
- **Interface Moderna**: PySide6 com design responsivo e cores personalizáveis
- **Processamento Paralelo**: Threads assíncronas para consultas simultâneas à API
- **Sistema de Configuração**: Gerenciamento persistente de configurações por empresa
- **Tela de Splash**: Animação de carregamento com progresso
- **Executável Autocontido**: Build modular com PyInstaller

## ✨ Funcionalidades

### 🏆 **Ranking de Lojas**
- Exibe ranking das melhores lojas baseado em custo e prazo
- Filtros por tipo de entrega (normal, retirada)
- Ordenação automática por melhor custo-benefício
- Destaque visual para top 3 posições
- Informações de estoque e transportadoras

### 📊 **Análise Detalhada**
- Visão detalhada de cada loja selecionada
- Comparação de opções de frete (entregas normais e retirada)
- Cálculo de prazos de entrega com datas estimadas
- Formatação de valores em moeda brasileira
- Informações de transportadoras e modalidades

### 📍 **Pontos de Retirada**
- Lista de pontos de retirada disponíveis por loja
- Endereços formatados e organizados
- Informações de distância e disponibilidade
- Tabela organizada com preços e prazos

### ❌ **Lojas Sem Entrega**
- Identificação de lojas sem opções de entrega
- Informações de estoque disponível
- Filtro por lojas nacionais
- Diferenciação entre estoque zerado e fora do range de CEP

### 📦 **Consulta de Estoque**
- Consulta simultânea em múltiplas lojas
- Visualização de estoque total e principal (1_1)
- Interface dedicada para análise de inventário
- Destaque visual para estoque baixo/zerado

### 📄 **Exportação JSON**
- Exportação completa dos dados em formato JSON
- Estrutura organizada para análise posterior
- Botão para copiar JSON para área de transferência
- Compatível com ferramentas de análise de dados

### ⚙️ **Sistema de Configuração**
- Configuração personalizada por empresa
- Gerenciamento de lojas e filiais com importação/exportação Excel
- Sistema de cores personalizável
- Tokens de autenticação VTEX
- Configurações de performance (workers, timeout)

## 🖥️ Interface

A aplicação possui uma interface moderna dividida em:

- **Painel Esquerdo**: Entrada de dados (CEP, SKU, seleção de lojas)
- **Painel Direito**: Resultados organizados em abas
- **Barra de Status**: Informações de progresso e status
- **Sistema de Abas**: Organização clara das funcionalidades
- **Tela de Splash**: Animação de carregamento com progresso

### Componentes da Interface
- **InputPanel**: Painel de entrada com validação de CEP e SKU
- **HeaderWidget**: Cabeçalho personalizado com nome da empresa
- **StatusBarWidget**: Barra de status com mensagens coloridas
- **SplashScreen**: Tela de carregamento com animação

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Windows 10/11
- Conexão com internet
- Conta VTEX com API habilitada

### Instalação Manual

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/vtex-freight-calculator.git
cd vtex-freight-calculator
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação:**
```bash
python main.py
```

### Instalação via Executável

1. **Baixe o executável:**
   - `SimuladorFrete2025_Modular.exe`

2. **Execute o arquivo:**
   - Duplo clique no executável
   - A aplicação será executada automaticamente

## 🚀 Como Usar

### 1. **Configuração Inicial**
- Abra a aplicação
- Vá para a aba "⚙️ Configurações"
- Clique em "🔧 Configurar Empresa"
- Preencha as informações da sua empresa:
  - Nome da empresa
  - Conta principal VTEX
  - App Key e App Token
  - Lista de lojas (pode importar do Excel)

### 2. **Simulação de Frete**
- **Digite o CEP** de destino (formato: 00000-000)
- **Selecione o SKU** do produto (histórico automático)
- **Escolha as lojas** para simular (filtro disponível)
- **Clique em "▶ SIMULAR FRETE"**

### 3. **Análise dos Resultados**
- **🏆 Ranking**: Melhores opções de frete ordenadas
- **📊 Detalhada**: Análise por loja com seletor
- **📍 Retirada**: Pontos de retirada organizados
- **❌ Sem Entrega**: Lojas sem opções com filtro
- **📦 Estoque**: Consulta de inventário
- **📄 JSON**: Dados completos para exportação

### 4. **Consulta de Estoque**
- Vá para a aba "📦 Estoque"
- Digite o SKU do produto
- Clique em "CONSULTAR ESTOQUE"
- Visualize o estoque por loja com destaque visual

## ⚙️ Configuração

### Configuração da Empresa

A aplicação permite configurar:

- **Informações da Empresa**:
  - Nome da empresa
  - Conta principal VTEX
  - App Key e App Token

- **Lojas e Filiais**:
  - Adicionar/remover lojas
  - Configurar códigos de filiais
  - Definir lojas nacionais
  - Importar/exportar lista via Excel

- **Configurações de Performance**:
  - Número máximo de workers
  - Timeout de requisições
  - SKU padrão
  - Histórico de SKUs recentes

### Estrutura de Configuração

```json
{
  "empresa": {
    "nome": "Sua Empresa",
    "conta_principal": "sua-empresa",
    "app_key": "sua-app-key",
    "app_token": "seu-app-token"
  },
  "lojas": [
    {
      "id": "loja-id",
      "nome": "Nome da Loja",
      "tipo": "Nacional",
      "nacional": true,
      "propriedade": "Própria",
      "conta_principal": false
    }
  ],
  "configuracoes": {
    "sku_padrao": "149718",
    "max_skus_recentes": 5,
    "max_workers": 20,
    "timeout_requests": 10
  },
  "cores": {
    "primaria": "#E91E63",
    "secundaria": "#FFFFFF",
    "destaque": "#E91E63",
    "fundo": "#FFFFFF",
    "texto": "#333333",
    "borda": "#F5F5F5",
    "destaque2": "#C2185B"
  }
}
```

## 🔧 Gerando o Executável

### Método Automático

1. **Execute o script de build:**
```bash
python build_encrypted.py
```

2. **O script irá:**
   - Verificar dependências
   - Instalar PyInstaller se necessário
   - Criar o executável modular
   - Limpar arquivos temporários

### Método Manual

1. **Instale o PyInstaller:**
```bash
pip install pyinstaller
```

2. **Execute o comando:**
```bash
pyinstaller --onefile --windowed --name=SimuladorFrete2025 --icon=entrega-rapida.ico main.py
```

### Características do Executável

- **Modular**: Todos os módulos integrados
- **Autocontido**: Não precisa de instalação Python
- **Portável**: Pode ser copiado para qualquer lugar
- **Configurável**: Sistema de configuração integrado
- **Persistente**: Configurações salvas na pasta do usuário

## 📋 Requisitos

### Sistema
- **OS**: Windows 10/11
- **RAM**: 4GB mínimo, 8GB recomendado
- **Espaço**: 100MB para instalação
- **Internet**: Conexão estável

### Dependências Python
```
PySide6>=6.0.0
requests>=2.25.0
pyinstaller>=4.0
openpyxl>=3.0.0
```

### API VTEX
- Conta VTEX ativa
- App Key e App Token válidos
- Permissões de API habilitadas

## 🏗️ Arquitetura

### Estrutura do Projeto

```
simulador-de-frete/
├── main.py                 # Classe principal FreteSimulator
├── config_manager.py       # Gerenciador de configurações persistente
├── config_ui.py           # Interface de configuração com Excel
├── ui_components.py       # Componentes de UI (InputPanel, Header, Status)
├── utils.py               # Funções utilitárias (validação, formatação)
├── threads.py             # Threads de processamento paralelo
├── splash_screen.py       # Tela de splash com animação
├── build_encrypted.py     # Script de build modular
├── tabs/                  # Módulos de abas
│   ├── __init__.py
│   ├── ranking_tab.py     # Aba de ranking com tabela
│   ├── resumo_tab.py      # Aba de resumo detalhado
│   ├── retirada_tab.py    # Aba de pontos de retirada
│   ├── estoque_tab.py     # Aba de consulta de estoque
│   ├── sem_entrega_tab.py # Aba de lojas sem entrega
│   └── json_tab.py        # Aba de exportação JSON
├── entrega-rapida.ico     # Ícone da aplicação
├── VTEX_Logo.svg.png      # Logo VTEX
└── README.md
```

### Componentes Principais

- **FreteSimulator**: Classe principal da aplicação
- **ConfigManager**: Gerenciamento de configurações com persistência
- **InputPanel**: Painel de entrada de dados com validação
- **StatusBarWidget**: Barra de status com mensagens coloridas
- **SimulacaoThread**: Thread para processamento paralelo de simulação
- **EstoqueThread**: Thread para consulta paralela de estoque

### Fluxo de Dados

1. **Entrada**: CEP, SKU, lojas selecionadas
2. **Validação**: Validação de CEP e SKU
3. **Processamento**: Threads assíncronas para API VTEX
4. **Análise**: Cálculo de custos, prazos e estoque
5. **Exibição**: Resultados organizados em abas
6. **Persistência**: Configurações salvas automaticamente

### APIs Utilizadas

- **Simulação de Frete**: `/api/checkout/pub/orderForms/simulation`
- **Políticas de Envio**: `/api/logistics/pvt/shipping-policies`
- **Consulta de Estoque**: `/api/logistics/pvt/inventory/skus/{sku}`

## 🤝 Contribuição

### Como Contribuir

1. **Fork** o projeto
2. **Crie** uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra** um Pull Request

### Padrões de Código

- Use **PEP 8** para estilo de código
- Documente funções e classes
- Teste suas mudanças
- Mantenha compatibilidade com Python 3.8+

### Reportar Bugs

Use o sistema de **Issues** do GitHub para reportar bugs e solicitar features.

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🆘 Suporte

### Problemas Comuns

**❓ A aplicação não inicia**
- Verifique se o Python 3.8+ está instalado
- Execute `pip install -r requirements.txt`

**❓ Erro de API VTEX**
- Verifique se os tokens estão corretos
- Confirme se a conta tem permissões de API

**❓ Executável não funciona**
- Execute como administrador
- Verifique se o antivírus não está bloqueando

**❓ Configurações não salvam**
- Verifique permissões de escrita na pasta do usuário
- Pasta: `C:\Users\[Usuário]\VTEX_Freight_Calculator\`

### Contato

- **GitHub Issues**: Para bugs e sugestões
- **Email**: [seu-email@exemplo.com]
- **Documentação**: [Link para documentação completa]

---

<div align="center">

**Desenvolvido com ❤️ para a comunidade VTEX**

![VTEX](https://img.shields.io/badge/VTEX-Partner-red.svg)
![Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)

</div>
