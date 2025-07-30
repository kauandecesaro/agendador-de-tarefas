# 📅 Agendador de Tarefas com AWS

Projeto completo que permite criar tarefas com data e horário, armazená-las no DynamoDB e receber lembretes por e-mail antes da execução usando serviços serverless da AWS.

---

## ✅ Visão Geral

Este projeto foi desenvolvido com o objetivo de aplicar conceitos de computação em nuvem (AWS), automações com Lambda e interação via linha de comando (CLI). O sistema permite:

- Agendar tarefas com título, descrição, horário de execução e lembrete.
- Enviar automaticamente lembretes por e-mail via SES.
- Gerenciar tarefas expiradas marcando-as como processadas.
- Interface simples por terminal (CLI) para criação, listagem e exclusão de tarefas.

---

## 🛠️ Tecnologias e Serviços Utilizados

- **Python 3.9**
- **AWS Lambda**
- **Amazon DynamoDB**
- **Amazon SES (Simple Email Service)**
- **Amazon EventBridge**
- **IAM (Roles e Policies)**
- **AWS CLI / Boto3**
- **VS Code + Git + GitHub**

---

## 🚀 Funcionalidades

| Função                    | Descrição |
|--------------------------|-----------|
| Criar tarefa             | Via CLI com data de execução e lembrete |
| Listar tarefas           | Exibe tarefas atuais do DynamoDB |
| Deletar tarefa           | Exclui tarefa pelo ID |
| Enviar lembrete          | Lambda envia e-mail quando chega a hora do lembrete |
| Processar expiradas      | Marca tarefas expiradas como processadas para evitar duplicidade |
| Agendamento automático   | EventBridge dispara funções Lambda periodicamente |

---

## ⚙️ Estrutura do Projeto

```bash
📁 agendador_tarefas_aws/
│
├── cli_tarefas.py                 # Interface CLI para criar, listar e deletar tarefas
├── lambda_processar_expiradas.py # Lambda para marcar tarefas expiradas como processadas
├── lambda_enviar_lembrete.py     # Lambda para envio de e-mails via SES
├── requirements.txt              # Dependências do projeto (ex: boto3)
├── README.md                     # Documentação do projeto
└── .env (opcional)               # Variáveis de ambiente locais


📦 Como rodar localmente
# Clone o repositório
git clone https://github.com/kauandecesaro/agendador_tarefas_aws.git
cd agendador_tarefas_aws

# Crie e ative seu ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

☁️ Deploy na AWS
Crie uma tabela DynamoDB chamada TarefasAgendadas com chave primária id (string).

Configure um e-mail verificado no Amazon SES para envio de lembretes.

Suba as funções Lambda:

lambda_enviar_lembrete.py

lambda_processar_expiradas.py

Configure roles IAM com políticas que autorizem acesso a DynamoDB e SES.

Crie regras no EventBridge para disparar as funções Lambda com periodicidade adequada.

Configure as variáveis de ambiente nas Lambdas, incluindo TAREFAS_TABLE_NAME.

📬 Exemplo de Uso

Criar uma nova tarefa via CLI:
bash
Copiar
Editar
python cli_tarefas.py
Você será guiado a informar título, descrição, data de execução, horário do lembrete e e-mail.

Listar tarefas:
bash
Copiar
Editar
python cli_tarefas.py --listar
Deletar tarefa:
bash
Copiar
Editar
python cli_tarefas.py --deletar <id-da-tarefa>

🧠 O que aprendi com este projeto
Uso prático do DynamoDB com boto3 em Python.

Configuração e envio de e-mails com Amazon SES.

Automação de processos usando AWS Lambda e EventBridge.

Configuração de permissões IAM para segurança e boas práticas.

Desenvolvimento de CLI simples para facilitar a interação.

Deploy e testes de funções serverless integradas.

👤 Sobre o autor
Desenvolvido por Kauan de Césaro

🌍 Desenvolvedor em formação

☁️ Entusiasta de computação em nuvem (AWS)

🧠 Estudante de Análise e Desenvolvimento de Sistemas - UNINTER

🇮🇹 Baseado na Itália

LinkedIn | GitHub
