from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='following', blank=True)
    email = models.EmailField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def get_following(self):
        return self.following.all()
    
    
    def get_followers(self):
        qs = Profile.objects.all()     
        followers_list = []
        for profile in qs:
            if self.user in profile.get_following():
                followers_list.append(profile)
        return followers_list
    
    
    def profiles_posts(self):
        return self.post_set.all()
        
    def __str__(self):
        return str(self.user.username)
    
    class Meta:
        ordering = ('-created',)


class Post(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    read = models.ManyToManyField(User, related_name='read', blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def get_author(self):
            return self.author


    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('-created',)
    
    READ_CHOICES = {
        ('Read', 'Read',),
        ('UnRead', 'UnRead',),
    }