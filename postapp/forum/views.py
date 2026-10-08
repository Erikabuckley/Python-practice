from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.signals import request_finished
#from django.core.mail import send_mail

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView

from forum.models import Post, Comment

from datetime import datetime

def my_callback(sender, **kwargs):
    print("Request finished")
    #send_mail("s","m",from_email='from@hmail.com',recipient_list=['to@gmail.com'],fail_silently=False)
request_finished.connect(my_callback)

def index(request):
    request.session.clear()
    messages.add_message(request, messages.INFO, 'Hello World')
    return HttpResponse('<html><body>Hello</body></html>')

class TestTemplateView(TemplateView):
    template_name = 'test_template.html'

class PostListView(ListView):
    model = Post
    context_object_name = "post_data"
    
    def get_queryset(self):
        self.queryset = Post.objects.all()
        if self.kwargs.get('year'):
           self.queryset = self.queryset.filter(created_at__year=self.kwargs['year'])        
        if self.kwargs.get('month'):
           self.queryset = self.queryset.filter(created_at__month=self.kwargs['month']) 
        return self.queryset
        
    def render_to_response(self, context, **response_kwargs):
        first_viewed = self.request.session.get('first_viewed', False)
        if first_viewed:
            return HttpResponse(f'You first viewed on {first_viewed}.')
        
        self.request.session['first_viewed'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        message_content = ''
        storage = get_messages(self.request)
        for message in storage:
            message_conent += f'<li{message}</li>'
        
        posts = ''    
        for post in context['post_data']:
            posts += f'<li{post.title}</li>'
        return HttpResponse(f'<html><body><ul>{posts}</ul><ul>{message_content}</ul></body</html>')

class PostDetailView(DetailView):
    model = Post
    def render_to_response(self, context, **response_kwargs):
        post = context.get('object')
        return HttpResponse(f'<html><body><ul><li>Title: {post.title}</li><li>Body: {post.body}</li><li>User: {post.user.first_name}</li></ul></body</html>')

class CommentListView(ListView):
    model = Comment
    context_object_name = 'comment_data'
    
    def get_queryset(self):
        self.queryset = Comment.objects.filter(post__id=self.kwargs['post_id'])
        return self.queryset
    
    def render_to_response(self, context, **response_kwargs):
        comments = ''
        for comment in context['comment_data']:
            comments += f'<li>{comment.body}</li>'
        return HttpResponse(f'<html><body><ul>{comments}</ul></body></html>')