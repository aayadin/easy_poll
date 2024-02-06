from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils.datastructures import MultiValueDictKeyError

from .functions import calculate_result, get_next_question, save_answer
from .models import Option, Poll


def index(request):
    polls = Poll.objects.all()
    return render(request, 'polls/index.html', {'polls': polls})


@login_required()
def poll(request, id, option=None):
    user = request.user
    try:
        option = request.GET['option']
        try:
            save_answer(user, int(option))
        except ValidationError:
            return redirect('index', request)
    except MultiValueDictKeyError:
        pass
    question = get_next_question(user, id, option)
    if question is None:
        results = calculate_result(id)
        return render(request, 'polls/results.html', context=results)
    options = Option.objects.filter(question=question)
    poll = Poll.objects.get(id=id)
    context = {
        'question': question.text,
        'options': options,
        'poll': poll
    }
    return render(request, 'polls/question.html', context)
