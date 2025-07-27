import json
import boto3
import os
import time
import uuid

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME')  # nome da tabela vindo da variável de ambiente
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # O corpo da requisição virá como string JSON
        body = json.loads(event.get('body', '{}'))
        
        mensagem = body.get('mensagem')
        tempo_expiracao_minutos = int(body.get('tempo_expiracao_minutos', 10))  # default 10 minutos
        
        if not mensagem:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'O campo "mensagem" é obrigatório'})
            }
        
        # Cria um ID único para a tarefa
        tarefa_id = str(uuid.uuid4())
        
        # Calcula o timestamp TTL em segundos Unix
        ttl = int(time.time()) + tempo_expiracao_minutos * 60
        
        # Monta o item para o DynamoDB
        item = {
            'id': tarefa_id,
            'mensagem': mensagem,
            'ttl': ttl
        }
        
        # Salva no DynamoDB
        table.put_item(Item=item)
        
        return {
            'statusCode': 201,
            'body': json.dumps({
                'id': tarefa_id,
                'mensagem': mensagem,
                'ttl': ttl
            })
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }