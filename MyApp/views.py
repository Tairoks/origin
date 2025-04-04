from django.shortcuts import render
from .models import Topic

def index (request):
    """Home view"""
    return render(request, 'myapp/index.html')

def topics(request):
    """Views topics"""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'MyApp/topics.html', context)
