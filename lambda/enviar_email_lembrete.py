import boto3
from boto3.dynamodb.conditions import Attr
from datetime import datetime, timezone
import json
import os

dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses', region_name='eu-central-1')  # ajuste se estiver em outra região

# Nome da sua tabela DynamoDB
TABELA = 'TarefasAgendadas'
REMETENTE = 'drinkcsgo@hotmail.com'  # email verificado no SES

def lambda_handler(event, context):
    agora = datetime.now(timezone.utc)

    tabela = dynamodb.Table(TABELA)

    # Busca tarefas com lembrete_em <= agora e lembrete_enviado == false
    try:
        response = tabela.scan(
            FilterExpression=Attr('lembrete_enviado').eq(False) & Attr('lembrete_em').lte(agora.isoformat())
        )
        tarefas = response.get('Items', [])
    except Exception as e:
        print("Erro ao buscar tarefas:", e)
        return {"statusCode": 500, "body": "Erro ao buscar tarefas."}

    tarefas_enviadas = 0

    for tarefa in tarefas:
        try:
            destinatario = tarefa['email']
            assunto = f"Lembrete: {tarefa['titulo']}"
            corpo = f"""Olá,

Este é um lembrete para a tarefa:

Título: {tarefa['titulo']}
Descrição: {tarefa['descricao']}
Execução prevista para: {tarefa['data_execucao']}

Até logo!
"""

            # Envia o email
            ses.send_email(
                Source=REMETENTE,
                Destination={'ToAddresses': [destinatario]},
                Message={
                    'Subject': {'Data': assunto},
                    'Body': {
                        'Text': {'Data': corpo}
                    }
                }
            )

            # Atualiza o campo lembrete_enviado para true
            tabela.update_item(
                Key={'id': tarefa['id']},
                UpdateExpression='SET lembrete_enviado = :val',
                ExpressionAttributeValues={':val': True}
            )

            tarefas_enviadas += 1
            print(f"Email enviado para {destinatario} com sucesso.")

        except Exception as e:
            print(f"Erro ao processar tarefa {tarefa.get('id')}: {e}")

    return {
        'statusCode': 200,
        'body': f"{tarefas_enviadas} lembretes enviados com sucesso."
    }
