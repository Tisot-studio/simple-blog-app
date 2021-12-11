from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView
from itertools import chain
from .forms import PostForm


# Домашняя страница
def index(request):
	return render(request, 'base/index.html')


# Мой профиль
def my_profile(request):
    user = Profile.objects.get(user=request.user)
    following = user.following.all()
    context = {'list': following}
    return render(request, 'base/profile.html', context)


# Список блогов
class ProfileListView(ListView):
    model = Profile
    template_name = 'base/main.html'
    context_object_name = 'profiles'
    
    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user)
    
 
# Просмотр блога
class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'base/detail.html'
    
    def get_object(self, **kwargs):
        pk = self.kwargs.get('pk')
        view_profile = Profile.objects.get(pk=pk)
        return view_profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_profile = self.get_object()
        my_profile = Profile.objects.get(user=self.request.user)
        if view_profile.user in my_profile.following.all():
            follow = True
        else:
            follow = False
        context = {'follow': follow,
                   'object': view_profile}
        return context


 # Кнопка подписки/отписки на блог  
def follow_unfollow_profile(request):
    if request.method == "POST":
        my_profile = Profile.objects.get(user = request.user)
        pk = request.POST.get('profile_pk')
        obj = Profile.objects.get(pk=pk)
        
        # Получаю список постов в которых автор нужный нам обьект
        obj_posts = []
        posts = Post.objects.all()
        for post in posts:
            if post.author == obj:
                obj_posts.append(post)     

        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
            
            # При отписке будет удаляться отметка о прочитанности поста, автором которого является обьект
            for p in obj_posts:
                p.read.remove(request.user)
        else:
            my_profile.following.add(obj.user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('base:blogs-list-view')


# Моя лента с постами
def posts_of_following_profiles(request):
    profile = Profile.objects.get(user=request.user)
    users = [user for user in profile.following.all()]
    
    # Создаю пустой список, куда буду добавлять посты тех на кого я подписан и свои посты (по необходимости), это моя лента
    posts = []
    qs = None
    
    for u in users:
        p = Profile.objects.get(user=u)
        p_posts = p.post_set.all()
        posts.append(p_posts)
    
    # Так можно добавить в список свои посты и отобразить например на отдельной странице. Сейчас будет отобрадаться только лента с постами интеерсных мне блогов.
    # my_posts = profile.profiles_posts()
    # posts.append(my_posts) 
    
    if len(posts) > 0:
        qs = sorted(chain(*posts), reverse=True, key=lambda obj : obj.created)
    return render(request, 'base/profile.html', {'profile':profile, 'posts': qs})


# Создаем пост
def new_post(request):
    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(data=request.POST)
        profile = Profile.objects.get(user=request.user)
        if form.is_valid():
            new_post = form.save(commit=False) 
            new_post.author = profile
            new_post.save()
            return redirect('base:my-profile')
    return render(request, 'base/new_post.html', {'form': form})


# Получаем нужный пост
def get_post(request, pk):
    post = Post.objects.get(id=pk)
    print(post.content)
    return render(request, 'base/post.html', {'post': post})


# Пометка о прочитанном посте
def read_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        
        if user in post_obj.read.all():
            post_obj.read.remove(user)
        else:
            post_obj.read.add(user)
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('base:post-detail-view')
