import boto3
import json

ses = boto3.client('ses')

def lambda_handler(event, context):
    destinatario = event.get('email')
    assunto = "Lembrete de tarefa"
    corpo = f"Olá, lembrete da sua tarefa: {event.get('descricao')} para {event.get('data_execucao')}"

    response = ses.send_email(
        Source='drinkcsgo@hotmail.com',  # coloque seu email verificado aqui
        Destination={'ToAddresses': [destinatario]},
        Message={
            'Subject': {'Data': assunto},
            'Body': {'Text': {'Data': corpo}}
        }
    )
    return {
        'statusCode': 200,
        'body': json.dumps(f"E-mail enviado para {destinatario}")
    }
