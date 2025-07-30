import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
tabela = dynamodb.Table(os.environ['NOME_TABELA'])

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        tarefa_id = body.get('id')

        if not tarefa_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'O campo "id" é obrigatório'})
            }

        tabela.delete_item(Key={'id': tarefa_id})

        return {
            'statusCode': 200,
            'body': json.dumps({'mensagem': f'Tarefa com ID {tarefa_id} deletada com sucesso'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
