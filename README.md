# Тестовое задание: Cоздание сервиса опросов с учетом пользователя и динамическим отображением вопросов.
[ссылка на задание](https://nomia2.notion.site/Python-developer-7adf62ee6a9f4aaab28db4ac661e2139)
## Описание ##
### В проекте реализованы: ###
1) Базовая система авторизации (регистрация, логин, логаут, смена пароля)
2) Главная страница со списком опросов
3) Страница с вопросами и результатами
4) Создание опросов через админку, с возможностью построения дерева ответов. Для настройки дерева нужно выбрать, какой вопрос показывать после какого ответа.

- Функции для получения статистики с использованием SQL находятся в polls/functions.py
- Прохождение опроса возмжно после регистрации и входа в систему.
- Результаты опроса показываются только если пройти опрос.
- Опрос начинается с последнего неотвеченного вопроса.
- База данных SQLite, проект демонстрационный.
- Для наглядности база данных загружена в репозиторий, там уже есть опросы, которые можно пройти.
- Также для упрощения проверки не исключены миграции.
- Никакие переменные не включались в .env, проект демонстрационный.

superuser: admin
password: admin

## Запуск приложения ##
- клонировать репозиторий
```
git git@github.com:aayadin/easy_poll.git
```
- установить требуемые пакеты:
```
pip install -r requirements.txt
```
- создать миграции (опционально):
```
python manage.py makemigrations
```
- применить миграции (опционально):
```
python manage.py migrate
```
- запустить сервер:
```
python manage.py runserver
```

Запуск по умолчанию на 127.0.0.1:8000

### Скрины ###
Главная:
<image src="https://github.com/aayadin/easy_poll/blob/main/static/screenshots/index.png">

Опрос:
<image src="https://github.com/aayadin/easy_poll/blob/main/static/screenshots/poll_in_progress.png">

Статистика по вопросам:
<image src="https://github.com/aayadin/easy_poll/blob/main/static/screenshots/question_results.png">

Статистика по ответам:
<image src="https://github.com/aayadin/easy_poll/blob/main/static/screenshots/answer_results.png">

Выполнил Андрей Ядин.
