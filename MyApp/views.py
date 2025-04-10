from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect
from .models import Topic
from .forms import TopicForm


def index (request):
    """Home view"""
    return render(request, 'myapp/index.html')

def topics(request):
    """Views topics"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'MyApp/topics.html', context)

def topic(request, topic_id):
    """View topic"""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'MyApp/topic.html', context)

def new_topic(request):
    """Create new topic"""
    if request.method != 'POST':
        # Data not sent, empty form created
        form = TopicForm()
    else:
        # POST data sent, process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('MyApp:topics')
    context = {'form': form}
    return render(request, 'myapp/new_topic.html', context)
