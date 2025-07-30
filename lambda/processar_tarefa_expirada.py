import boto3
import os
from datetime import datetime, timezone
from boto3.dynamodb.conditions import Attr

# DynamoDB
dynamodb = boto3.resource('dynamodb')
tabela = dynamodb.Table(os.environ['TAREFAS_TABLE_NAME'])

# SES
ses = boto3.client('ses', region_name='us-east-1')  # ajuste se estiver em outra região

REMETENTE = "drinkcsgo@hotmail.com"  # e-mail verificado no SES

def lambda_handler(event, context):
    # Obter hora atual em UTC
    agora = datetime.now(timezone.utc)

    # Buscar tarefas não processadas e com data/hora no passado
    resposta = tabela.scan(
        FilterExpression=Attr('processado').eq(False) & Attr('data_hora').lt(agora.isoformat())
    )
    
    tarefas_expiradas = resposta.get('Items', [])

    for tarefa in tarefas_expiradas:
        try:
            # Enviar e-mail
            ses.send_email(
                Source=REMETENTE,
                Destination={'ToAddresses': [tarefa['email']]},
                Message={
                    'Subject': {'Data': 'Tarefa Expirada'},
                    'Body': {
                        'Text': {
                            'Data': f"Sua tarefa '{tarefa['descricao']}' expirou em {tarefa['data_hora']}."
                        }
                    }
                }
            )
            
            # Atualizar tarefa como processada
            tabela.update_item(
                Key={'id': tarefa['id']},
                UpdateExpression="set processado = :val",
                ExpressionAttributeValues={':val': True}
            )
        except Exception as e:
            print(f"Erro ao processar tarefa {tarefa['id']}: {str(e)}")
    
    return {
        'statusCode': 200,
        'body': f"{len(tarefas_expiradas)} tarefas processadas."
    }
