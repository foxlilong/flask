from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import Question, Choice


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    data = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context=data)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "Question result is: %s"
    return HttpResponse(response % question_id)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        select_choice = question.choice_set.get(pk=request.POST['choice'])
        print(select_choice)
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question,
                                                     'error_message': "You didn't select a choice"})
    else:
        select_choice.votes += 1
        select_choice.save()

    return HttpResponseRedirect(reverse('polls:result', args=(question_id,)))
