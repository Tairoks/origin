from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404


def index (request):
    """Home view"""
    return render(request, 'myapp/index.html')

@login_required
def topics(request):
    """Views topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'MyApp/topics.html', context)

@login_required
def topic(request, topic_id):
    """View topic"""
    topic = Topic.objects.get(id=topic_id)
    #Checking the authorized user
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'MyApp/topic.html', context)

@login_required
def new_topic(request):
    """Create new topic"""
    if request.method != 'POST':
        # Data not sent, empty form created
        form = TopicForm()
    else:
        # POST data sent, process data
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('MyApp:topics')
    context = {'form': form}
    return render(request, 'myapp/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Create entry"""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Data not sent, empty form created
        form = EntryForm()
    else:
        # POST data sent, process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('MyApp:topic', topic_id=topic_id)
    context = {'topic': topic, 'form': form}
    return render(request, 'myapp/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edits an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        #the form is filled current data
        form = EntryForm(instance=entry)
    else:
        #Sending data
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid:
            form.save()
            return redirect('MyApp:topic', topic_id=topic.id)
    context = {"topic": topic, "form": form, 'entry': entry}
    return render(request, 'myapp/edit_entry.html', context=context)
