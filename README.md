# Тестовое задание: Cоздание сервиса опросов с учетом пользователя и динамическим отображением вопросов.
[ссылка на задиние](https://nomia2.notion.site/Python-developer-7adf62ee6a9f4aaab28db4ac661e2139)
## Описание ##
### В проекте реализованы: ###
1) Базовая система авторизации (регистрация, логин, логаут, смена пароля)
2) Главная страница со списком опросов
3) Страница с вопросами и результатами
4) Создание опросов через админку, с возмодностью построения дерева ответов. Для настройки дерева нужно выбрать, какой вопрос показывать после какого ответа.

- Функции для получения статистики с использованием SQL находятся в polls/functions.py
- Прохождение опроса возмжно после регистрации и входа в систему.
- Результаты опроса показвыаются только если пройти опрос.
- Опрос начинается с последнего неотвеченного вопроса.
- База данных SQLite, проект демонтрационный.
- Для наглядности база данных загружена в репозиторий, там уже есть опросы, которые можно пройти.
- Также для упрощения проверки не не исключены миграции.
- Никакие переменные не включались в .env, проект демонтрационный.

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
- применить пиграции (опционально):
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

Опрос:

Статистика по вопросам:

Статистика по ответам:

Выполнил Андрей Ядин.