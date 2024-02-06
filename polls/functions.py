from typing import Optional, Type

from django.core.exceptions import ValidationError
from django.db import connection
from django.utils.functional import SimpleLazyObject

from .models import Answer, Option, Question


def get_next_question(user: Type[SimpleLazyObject],
                      poll_id: int,
                      option_id: Optional[int]) -> [Type[Question], None]:
    """
    Функция для получения следующего вопроса для отображения.
    """
    # если передан вариант ответа, то вызывается метод next_question
    if option_id:
        question = Option.objects.get(id=option_id).next_question
        return question
    # в противном случае берем первый вопрос из опроса
    question = Question.objects.filter(poll=poll_id)[0]
    # если у пользователя уже есть ответы в этом опросе,
    # показываем первый неотвеченный вопрос
    try:
        last_answer = Answer.objects.filter(user=user, poll=poll_id)[0]
        return last_answer.option.next_question
    except IndexError:
        # если функция вернула None, значит это был последний вопрос
        return question


def save_answer(user: Type[SimpleLazyObject], option_id: int) -> None:
    """
    Функция для сохранения ответа пользователя.
    """
    option = Option.objects.get(id=option_id)
    question = option.question
    if Answer.objects.filter(user=user, question=question).exists():
        raise ValidationError(
            'You have already answered to this question',
            code='answered'
        )
    poll = question.poll
    return Answer(
        user=user,
        option=option,
        question=question,
        poll=poll
    ).save()


def parse_question_result(question_stats: list[tuple]) -> list[dict]:
    """
    Функция для преобразования данных из БД в удобный для отрисовки формат
    """
    parsed_question_stats = []
    for question in question_stats:
        parsed_question_stats.append({
            'text': question[0],
            'rank': question[1],
            'total': question[2],
            'percent': (format(float(question[3]), '.2f') if question[3] else '-')
        })
    return parsed_question_stats


def parse_answer_result(answer_stats: list[list[tuple]]) \
        -> list[dict[str, list[dict[str, str]]]]:
    """
    Функция для преобразования данных из БД в удобный для отрисовки формат
    """
    parsed_answer_stats = []
    for question in answer_stats:
        option_stats = []
        question_stats = {f'{question[0][0]}': option_stats}
        for answer in question:
            option_stats.append({
                'text': answer[1],
                'total': answer[2],
                'percent': (format(float(answer[3]), '.2f') if answer[3] else '-')
            })
        parsed_answer_stats.append(question_stats)
    return parsed_answer_stats


def calculate_result(poll_id: int) -> dict:
    """
    Получение статистики из БД без использования ORM.
    """
    # Сначала просто получаем количсетво пользователей, которые прошли опрос
    with connection.cursor() as cursor:
        cursor.execute(f'''
            SELECT COUNT(DISTINCT user_id)
            FROM polls_answer
            WHERE poll_id = %s;
        ''', [poll_id])
        total_users = cursor.fetchone()[0]

    # Статистика по вопросам
    # Выводит расчет ранга и расчет процента ответивших
    with connection.cursor() as cursor:
        cursor.execute(f'''
            SELECT q.text,
                   DENSE_RANK() OVER (ORDER BY COUNT(DISTINCT a.user_id) DESC) AS question_rank,
                   COUNT(DISTINCT a.user_id) AS user_count,
                   COUNT(DISTINCT a.user_id) * 100.0 / NULLIF(
                       (SELECT COUNT(DISTINCT user_id) FROM polls_answer WHERE poll_id = %s AND question_id = %s), 0
                   ) AS user_percentage
            FROM polls_question q
            LEFT JOIN polls_answer a ON a.question_id = q.id AND a.poll_id = %s
            WHERE q.poll_id = %s
            GROUP BY q.id, q.text
            ORDER BY q.id;
        ''', [poll_id, poll_id, poll_id, poll_id])
        question_stats = cursor.fetchall()

    # Получаем список вопросов, относящихся к опросу
    with connection.cursor() as cursor:
        cursor.execute(f'''
            SELECT id
            FROM polls_question
            WHERE poll_id = %s
        ''', [poll_id])
        questions = cursor.fetchall()

    # По каждому вопросу получаем варианты ответов с расчетом доли ответивших.
    answer_stats = []
    for question in questions:
        with connection.cursor() as cursor:
            cursor.execute(f'''
                SELECT q.text,
                       o.text,
                       COUNT(DISTINCT a.user_id) AS option_user_count,
                       COUNT(DISTINCT a.user_id) * 100.0 / NULLIF(
                           (SELECT COUNT(DISTINCT user_id)
                           FROM polls_answer WHERE question_id = %s), 0
                       ) AS option_percentage
                FROM polls_option o
                LEFT JOIN polls_answer a ON a.option_id = o.id AND a.question_id = %s
                JOIN polls_question q ON o.question_id = q.id
                WHERE o.question_id = %s
                GROUP BY o.id, o.text
                ORDER BY o.id;
            ''', [question[0], question[0], question[0]])
            stats = cursor.fetchall()
            if stats:
                answer_stats.append(stats)

    result = {
        'total_users': total_users,
        'question_stats': parse_question_result(question_stats),
        'answer_stats': parse_answer_result(answer_stats)
    }
    return result
