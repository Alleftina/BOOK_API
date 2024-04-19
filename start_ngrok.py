import subprocess
import requests
import os
import time
from utils.config import NGROK_TOKEN
from loguru import logger

# Функция для запуска ngrok и получения HTTPS адреса
def get_ngrok_https_address():
    # Запускаем ngrok для проброса порта 5000
    subprocess.Popen(['ngrok', 'authtoken', NGROK_TOKEN], stdout=subprocess.PIPE)
    subprocess.Popen(['ngrok', 'http', '8000'], stdout=subprocess.PIPE)

    # Ждем несколько секунд для того, чтобы ngrok успел запуститься
    time.sleep(5)

    # Получаем данные о проброшенном адресе с помощью API ngrok
    response = requests.get('http://localhost:4040/api/tunnels')
    data = response.json()

    # Извлекаем HTTPS адрес из полученных данных
    https_address = data['tunnels'][0]['public_url']
    logger.info(https_address)
    return https_address


# Функция для запуска вашего Python файла с ботом на Flask
def run_flask_bot(ngrok_https_address):
    # Передаем полученный HTTPS адрес в качестве переменной окружения
    os.environ['NGROK_HTTPS_ADDRESS'] = ngrok_https_address
    cwd = os.getcwd()

    # Путь к скрипту активации виртуального окружения
    activate_venv = f'source {cwd}/venv/bin/activate'
    command = f'uvicorn main:app --host 0.0.0.0 --port 8000 --reload'
    # Запуск команды в терминале с предварительным включением venv
    subprocess.run(activate_venv, shell=True)
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    # Получаем HTTPS адрес от ngrok
    ngrok_https_address = get_ngrok_https_address()

    # Запускаем вашего бота на Flask с полученным HTTPS адресом
    run_flask_bot(ngrok_https_address)
