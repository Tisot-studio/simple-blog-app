from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import request
from .models import Profile, Post
from django.contrib.auth.models import User
from .utils import Util


# Автоматическое создание профиля при регистрации нового пользователя
@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Обновление email профиля при добавлении email в модель пользователя       
@receiver(post_save, sender=User)
def updateProfileEmail(sender, instance, **kwarg):
    user = instance
    pf = Profile.objects.get(user=user)
    if user.email != '':
        pf.email = user.email
        pf.save()        
   
   
# Отправка сообщения подписчикам при выходе нового поста          
@receiver(post_save, sender=Post)
def notify_followers(sender, instance, created, **kwargs):
    if created:
        me = instance.author
        followers = me.get_followers()       
        for follower in followers:
            url = f'http://localhost:8000/post/{instance.id}'
            email_body = f" {me} опубликовал новый пост: {url} "
            mail={'email_body': email_body, 'subject': 'new post', 'to': follower.email}
            Util.send_email(mail)
 



    


            
            