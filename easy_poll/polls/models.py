from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint

User = get_user_model()


class Poll(models.Model):
    title = models.CharField('Заголовок', max_length=255)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return self.title[:50]


class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.TextField('Текст вопроса', max_length=500)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['id']

    def __str__(self):
        return self.text[:50]


class Option(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='current'
    )
    next_question = models.ForeignKey(
        Question,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='next'
    )
    text = models.CharField(
        'Текст варианта ответа',
        max_length=255,
        blank=True
    )

    def clean(self):
        if self.question == self.next_question:
            raise ValidationError('Next question cannot be current question')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'

    def __str__(self):
        return self.text[:50]


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
        ordering = ['-id']
        constraints = [
            UniqueConstraint(
                fields=('user', 'question'),
                name='unique_question',
                violation_error_message='Cant answer twice on a same question'
            ),
        ]

    def __str__(self):
        return f'{self.user} answered: {self.option}'
