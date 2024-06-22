import os
import datetime
import pyttsx3
import speech_recognition as sr
import requests
import json
import pyautogui
import time

# Inicializar o motor de síntese de fala
engine = pyttsx3.init()

# Função para abrir programas
def abrir_programa(programa):
    try:
        os.system(programa)
    except Exception as e:
        print(f"Erro ao abrir o programa: {e}")

# Função para enviar mensagem ditada pelo usuário
def enviar_mensagem(mensagem):
    print(f"Mensagem enviada: {mensagem}")
    # Simular a digitação da mensagem no Notepad
    pyautogui.typewrite(mensagem)

# Função para mensagem de boas-vindas
def mensagem_boas_vindas():
    print("Bem-vindo de volta!")

# Função para obter o clima do dia
def obter_clima():
    cidade = "Brazil"
    API_key = "200490309488801d7b2664ca78c5aa75"  # Substitua "SuaAPIKey" pela sua chave de API da OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_key}&units=metric"
    response = requests.get(url)
    
    # Verificar se a resposta foi bem-sucedida
    if response.status_code == 200:
        data = response.json()
        # Verificar se a chave 'weather' existe no dicionário retornado
        if 'weather' in data:
            clima = data['weather'][0]['description']
            print(f"O clima para hoje em {cidade} é: {clima}")
        else:
            print("Não foi possível obter informações sobre o clima.")
    else:
        print("Erro ao obter dados do servidor.")

# Função para montar a agenda de afazeres do dia
def montar_agenda():
    agora = datetime.datetime.now()
    hora_atual = agora.hour
    if hora_atual < 12:
        print("Manhã: Faça o café da manhã e revise sua agenda.")
    elif hora_atual < 18:
        print("Tarde: Trabalhe em suas tarefas importantes.")
    else:
        print("Noite: Relaxe e descanse.")

# Função para reconhecer a fala do usuário e convertê-la em texto
def reconhecer_fala():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Fale algo:")
        audio = recognizer.listen(source)

    try:
        texto = recognizer.recognize_google(audio, language="pt-BR")
        print(f"Você disse: {texto}")
        return texto
    except sr.UnknownValueError:
        print("Não foi possível entender a fala.")
    except sr.RequestError as e:
        print(f"Erro na solicitação ao serviço de reconhecimento de fala; {e}")

# Função principal
def main():
    mensagem_boas_vindas()
    obter_clima()
    montar_agenda()
    
    # Exemplo de uso das outras funcionalidades
    abrir_programa("notepad.exe")

    # Aguardar um momento para o Notepad abrir completamente
    time.sleep(1)

    # Clicar na janela do Notepad para garantir que ele tenha o foco
    pyautogui.click()

    while True:
        # Reconhecer a fala do usuário
        texto_ditado = reconhecer_fala()

        # Se o usuário disse algo, digite no Notepad
        if texto_ditado:
            enviar_mensagem(texto_ditado)
            # Sintetizar a fala do usuário
            engine.say(texto_ditado)
            engine.runAndWait()

if __name__ == "__main__":
    main()
