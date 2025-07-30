import json
import boto3
import os
import time
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        agora = int(time.time())

        # Scan para encontrar tarefas expiradas e não processadas
        response = table.scan(
            FilterExpression=Attr('ttl').lt(agora) & (Attr('processado').not_exists() | Attr('processado').eq(False))
        )
        tarefas = response.get('Items', [])

        if not tarefas:
            return {
                'statusCode': 200,
                'body': json.dumps('Nenhuma tarefa expirada encontrada.')
            }

        for tarefa in tarefas:
            # Atualizar a tarefa marcando processado = True
            table.update_item(
                Key={'id': tarefa['id']},
                UpdateExpression="SET processado = :p",
                ExpressionAttributeValues={':p': True}
            )
            # Aqui pode ser inserida a lógica extra, tipo envio de e-mail, etc.

        return {
            'statusCode': 200,
            'body': json.dumps(f"{len(tarefas)} tarefas processadas com sucesso.")
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
