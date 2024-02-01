from django.db import models

from django.contrib.auth import get_user_model


User = get_user_model()
QUESTION_TYPES = ['radio', 'checkbox', 'form']


class Poll(models.Model):
    title = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    type = models.Choices(QUESTION_TYPES)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    previous = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='next'
    )

    def __str__(self):
        return self.text[:25]


class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} answered: {self.option}'
