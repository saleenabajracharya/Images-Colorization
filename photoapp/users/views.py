from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm,ProfileUpdateForm, UserUpdateForm
from django.views.generic import ListView, DetailView,UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from blog.models import Post
import os
import uuid
import cv2 
from django.conf import settings
from blog.util import colorMyImg
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import View

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created for {username} Login In Now!!!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    author = request.user
    posts = Post.objects.filter(author=author)
    return render(request, 'profile.html', {'author': author, 'posts': posts}) 

def profile_update(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
       
       
    context = {
        "u_form": u_form,
        "p_form": p_form
    }
    return render(request, 'profile_update.html',context)



class UserPostListView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'profile.html'
    context_object_name = 'posts'
    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(author=user).order_by('-date_posted')
        return queryset

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_detail.html'


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