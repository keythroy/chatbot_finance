from app.services.openai_service import OpenAIService

def clean_logs():
    with open('app/logs/app.log', 'w') as f:
        f.write('')

if __name__ == '__main__':

    clean_logs()

    openai = OpenAIService()
    openai.start_chat()


    # qual é a cotação da vale agora?
    


