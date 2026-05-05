-> O InvestVision IA é uma aplicação web completa que permite ao usuário:

Gerenciar sua carteira de investimentos
Acompanhar rentabilidade em tempo real
Visualizar gráficos interativos
Receber análises inteligentes com IA
Obter insights sobre diversificação e risco

- Funcionalidades

-> Autenticação

Login seguro
Cadastro de usuário
Logout com proteção CSRF

-> Carteira de Investimentos

CRUD completo de ativos
Suporte a ações (B3) e criptomoedas
Integração com Yahoo Finance (yfinance)

-> Dashboard Inteligente

Valor total investido
Valor atual da carteira
Lucro / prejuízo
Rentabilidade %

-> Score do Investidor

Avaliação automática baseada em:
Rentabilidade
Diversificação
Concentração de ativos

-> Análise com IA

Geração de insights personalizados
Botão interativo com animação
Efeito de digitação estilo ChatGPT

-> Gráficos

Evolução da carteira (linha)
Distribuição por ativos (doughnut)

-> Alertas Inteligentes

Alta concentração de ativos
Baixa diversificação
Risco elevado

--------------------------------------------------------------------

-> Tecnologias utilizadas

-> Backend

Python
Django
Django ORM

-> Frontend
HTML5
CSS3 
JavaScript

-> Dados e APIs

yfinance (dados de mercado)
OpenAI API (análise inteligente)

-> Visualização

Chart.js

----------------------------------------------------------------------

Instalação

cd investvision-ia

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Rodar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Rodar projeto
python manage.py runserver

--------------------------------------------------------------

Variáveis de ambiente (.env)

SECRET_KEY=sua_chave
DEBUG=True

OPENAI_API_KEY=sua_api_key