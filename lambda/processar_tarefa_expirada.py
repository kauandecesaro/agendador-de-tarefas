import boto3
import os
import time
import json

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    agora = int(time.time())

    try:
        response = table.scan(
            FilterExpression="#ttl_attr < :now",
            ExpressionAttributeNames={"#ttl_attr": "ttl"},
            ExpressionAttributeValues={":now": agora}
        )
        tarefas_expiradas = response.get('Items', [])

        if not tarefas_expiradas:
            return {
                'statusCode': 200,
                'body': json.dumps("Nenhuma tarefa expirada encontrada.")
            }

        for tarefa in tarefas_expiradas:
            print(f"Processando tarefa expirada: {tarefa}")

            # Deleta a tarefa após processar
            table.delete_item(Key={'id': tarefa['id']})

        return {
            'statusCode': 200,
            'body': json.dumps(f"{len(tarefas_expiradas)} tarefa(s) expiradas processadas.")
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
