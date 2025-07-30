import boto3
import uuid
from datetime import datetime
import re
from colorama import init, Fore, Style

# Inicializar colorama para cores no terminal
init(autoreset=True)

# Conexão com DynamoDB
dynamodb = boto3.resource('dynamodb')
tabela = dynamodb.Table('Tarefas')

# Validações
def validar_data_iso8601(data):
    try:
        datetime.strptime(data, "%Y-%m-%dT%H:%M:%SZ")
        return True
    except ValueError:
        return False

def validar_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

# Funções de operação
def adicionar_tarefa():
    print(Fore.CYAN + "\n📌 Adicionar nova tarefa")

    titulo = input("Título: ").strip()
    descricao = input("Descrição: ").strip()

    while True:
        data_execucao = input("Data de execução (YYYY-MM-DDTHH:MM:SSZ): ").strip()
        if validar_data_iso8601(data_execucao):
            break
        print(Fore.RED + "❌ Formato de data inválido.")

    while True:
        lembrete_em = input("Data para lembrete (YYYY-MM-DDTHH:MM:SSZ): ").strip()
        if validar_data_iso8601(lembrete_em):
            break
        print(Fore.RED + "❌ Formato de data inválido.")

    while True:
        email = input("E-mail para lembrete: ").strip()
        if validar_email(email):
            break
        print(Fore.RED + "❌ E-mail inválido.")

    tarefa = {
        "id": str(uuid.uuid4()),
        "titulo": titulo,
        "descricao": descricao,
        "data_execucao": data_execucao,
        "lembrete_em": lembrete_em,
        "email": email,
        "lembrete_enviado": False
    }

    try:
        tabela.put_item(Item=tarefa)
        print(Fore.GREEN + "✅ Tarefa adicionada com sucesso!")
    except Exception as e:
        print(Fore.RED + f"Erro ao adicionar tarefa: {e}")

def listar_tarefas():
    print(Fore.CYAN + "\n📋 Lista de Tarefas")
    try:
        response = tabela.scan()
        tarefas = response.get("Items", [])
        tarefas.sort(key=lambda x: x.get("data_execucao", ""))

        if not tarefas:
            print(Fore.YELLOW + "Nenhuma tarefa encontrada.")
            return

        for tarefa in tarefas:
            print(Style.BRIGHT + Fore.MAGENTA + f"\n🆔 {tarefa['id']}")
            print(Fore.WHITE + f"📌 Título: {tarefa['titulo']}")
            print(f"📝 Descrição: {tarefa['descricao']}")
            print(f"⏰ Execução: {tarefa['data_execucao']}")
            print(f"🔔 Lembrete: {tarefa['lembrete_em']}")
            print(f"📧 E-mail: {tarefa['email']}")
            print(f"✅ Enviado: {tarefa['lembrete_enviado']}")

    except Exception as e:
        print(Fore.RED + f"Erro ao listar tarefas: {e}")

def deletar_tarefa():
    print(Fore.CYAN + "\n🗑️ Deletar tarefa")
    id_tarefa = input("ID da tarefa: ").strip()
    confirm = input(Fore.YELLOW + f"Confirma exclusão da tarefa {id_tarefa}? (s/n): ").strip().lower()

    if confirm == "s":
        try:
            tabela.delete_item(Key={"id": id_tarefa})
            print(Fore.GREEN + "✅ Tarefa deletada com sucesso.")
        except Exception as e:
            print(Fore.RED + f"Erro ao deletar tarefa: {e}")
    else:
        print(Fore.YELLOW + "❌ Ação cancelada.")

def marcar_como_enviada():
    print(Fore.CYAN + "\n✅ Marcar tarefa como enviada")
    id_tarefa = input("ID da tarefa: ").strip()
    try:
        tabela.update_item(
            Key={"id": id_tarefa},
            UpdateExpression="SET lembrete_enviado = :val",
            ExpressionAttributeValues={":val": True}
        )
        print(Fore.GREEN + "Tarefa marcada como enviada com sucesso.")
    except Exception as e:
        print(Fore.RED + f"Erro ao atualizar tarefa: {e}")

# Menu
def menu():
    while True:
        print(Style.BRIGHT + Fore.BLUE + "\n=== Menu Principal ===")
        print("1. Adicionar tarefa")
        print("2. Listar tarefas")
        print("3. Marcar como enviada")
        print("4. Deletar tarefa")
        print("0. Sair")

        escolha = input("Escolha uma opção: ").strip()
        if escolha == "1":
            adicionar_tarefa()
        elif escolha == "2":
            listar_tarefas()
        elif escolha == "3":
            marcar_como_enviada()
        elif escolha == "4":
            deletar_tarefa()
        elif escolha == "0":
            print(Fore.BLUE + "👋 Saindo...")
            break
        else:
            print(Fore.RED + "❌ Opção inválida.")

# Execução
if __name__ == "__main__":
    menu()
