from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect 
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required





class NewsList (ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context
     
class NewDetail (DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
    queryset = Post.objects.all()


class Search (ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-id')
    #ordering = ['-price']
   
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) 
        return context 
    
class PostAdd (LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    template_name = 'new_add.html'
    form_class = PostForm
    permission_required = ('news.add_post')

class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'new_add.html'
    form_class = PostForm
    permission_required = ('news.change_post')
 
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
 
 
class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'new_delete.html'
    queryset = Post.objects.all()
    context_object_name = 'new'
    success_url = '/news/'
    permission_required = ('news.delete_post')


@login_required
def become_author(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
        Author.objects.create(userAuthor=request.user, ratingAuthor=0)
    return redirect("/news/")
    

