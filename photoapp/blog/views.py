from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Post
from . import util
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from blog.models import Post
from django.shortcuts import get_object_or_404
from django.views.generic import View
import os
import uuid
import cv2 
from django.conf import settings
from .util import colorMyImg

def about(request):
    return render(request,'about.html',{'title': "About Page"})



class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ["-date_posted"]
     
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'
    


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title',  'image']
    

    def form_valid(self, form):
        form.instance.author = self.request.user
        uploaded_image = form.cleaned_data['image']
    # Colorize the image
        colorized_image = colorMyImg(uploaded_image)
    # Save the colorized image to a file
        filename = str(uuid.uuid4()) + '.jpg'
        filepath = os.path.join(settings.MEDIA_ROOT, filename)
        cv2.imwrite(filepath, colorized_image)
    # Save the path of the saved image file to the database
        post = form.save(commit=False)
        post.image = filename
        post.save()
        return super().form_valid(form)

    # def test_func(self):
    #     post = self.get_object()
    #     if self.request.user == post.author:
    #         return True
    #     return False

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title',  'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        uploaded_image = form.cleaned_data['image']
    # Colorize the image
        colorized_image = colorMyImg(uploaded_image)
    # Save the colorized image to a file
        filename = str(uuid.uuid4()) + '.jpg'
        filepath = os.path.join(settings.MEDIA_ROOT, filename)
        cv2.imwrite(filepath, colorized_image)
    # Save the path of the saved image file to the database
        post = form.save(commit=False)
        post.image = filename
        post.save()
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



class ImageDownloadView(View):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        file_path = post.image.path
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename={}'.format(post.image.name.split('/')[-1])
            return response
        raise Http404




def search(request):
        query = request.GET['query']
        allPosts = Post.objects.filter(title__icontains=query).order_by("-date_posted")
        params = {'posts': allPosts, 'query':query}
        return render(request, 'search.html', params)


