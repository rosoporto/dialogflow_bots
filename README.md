# Боты-помошники в Telegram и VK с обработкой сообщений в нейросети
Боты помогают закрывать все типичные вопросы от пользователей. При обработке более сложных вопросов, боты будут перенаправлять пользователей на операторов.

## Как установить (на примере работы в среде Windows)
У вас уже должен быть установлен Python 3.

1. Установить виртуальное окружение и активировать его:
    ```shell
    python -m venv venv
    ./venv/Scripts/Activate.ps1
    ```

2. Клонировать репозиторий:
    ```shell
    git clone https://github.com/rosoporto/dialogflow_bots.git
    ```

3. Установить зависимости:
    ```shell
    pip install -r requirements.txt
    ```
4. Cоздать [бота](https://t.me/BotFather) в Telegram и получить API-токен вида:
    ```shell
    988463085:AGEArJ5Bde5DYfu8ElzVhNM
    ```
5. Создать группу в [VK](https://vk.com). Получите токен группы в настройках сообщества и разрешите боту отправку сообщений.

6. 1. [Создать агента DialogFlow](https://dialogflow.cloud.google.com/#/newAgent). В качестве языка по уполномочию установите русский. Скопировать ваш созданный Progect ID;
   2. [Получить файл `credentials.json`](https://cloud.google.com/dialogflow/es/docs/quick/setup#sdk) с ключами от вашего Google-аккаунта и положите этот файл в корень проекта. ВНИМАНИЕ! Файл хранит секретные данные; 
   4. [Включить API агента](https://cloud.google.com/dialogflow/es/docs/quick/setup#api).

7. Создать в корне проекта файл `.env` для хранения переменных с данными (токенами) от сервисов и заполнить его:
	```dotenv
	TG_BOT_TOKEN= ... API-токен от бота в Telegram
	TG_CHAT_ID= ... Ваш личный ID в в Telegram
	PROJECT_ID= ... ID агента DialogFlow 
	GOOGLE_APPLICATION_CREDENTIALS= ... Путь к файлу credentials.json, в котором лежат данные для аутентификации в Google Clod Services
	VK_GROUP_TOKEN= ... Токен группы ВКонтакте
	```

8. Обучить нейросеть Dialogflow:
    1. [Вручную](https://cloud.google.com/dialogflow/es/docs/intents-training-phrases);
    2. Через JSON файл:
      1. Заполнить JSON файл с именем `questions.json` в папке `training` проекта;      
      2. Запустить скрипт:
        ```shell
        python training_dialogflow.py
        ```

## Как запустить

1. Telegram:
	```shell
	python tg_bot.py
	```
2. VK:
	```shell
	python vk_bot.py
    ```
    
### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).