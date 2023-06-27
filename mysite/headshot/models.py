from pyexpat import model
from django.db import models
from django.contrib.auth.models import User 

#models:
# - shot: pic, bio, user, time, likers (m2m user)
# - hashtags: hash_text, shots (m2m shot)
# - user: pfp, bio
# - mention: show to user or not, time


class Shot(models.Model):    
    shot_pic = models.ImageField(upload_to='images')
    shot_text = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    time_pub = models.DateTimeField('date published', auto_now_add=True)
    likers = models.ManyToManyField(User, related_name='likers')
    mentions = models.ManyToManyField(User, through='Mention')

    def __str__(self):
        return f'{self.id} - {self.shot_text} - {self.author.username}'

class Comment(models.Model):
    comment_pic = models.ImageField(upload_to='images')
    comment_text = models.CharField(max_length=255)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_author')
    shot = models.ForeignKey(Shot, on_delete=models.CASCADE, null=True)   
    likers_comment = models.ManyToManyField(User, related_name='likers_comment')
    mention_comment = models.ManyToManyField(User, through='Comment_mention', related_name='mention_comment')

class Hashtag(models.Model):
    hashtag_text = models.CharField(max_length=100)
    shots = models.ManyToManyField(Shot)
    

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_pfp = models.ImageField(upload_to='images/users', blank=True)
    bio = models.CharField(max_length=255, blank=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)

    def __str__(self) -> str:
        return f'{self.user.username} - {self.user.id} (UserProfile id: {self.id})' 

class Mention(models.Model):
    # 1-m many to a post, 1-m with a comment, 1-m with a user
    shot = models.ForeignKey(Shot, on_delete=models.CASCADE)
    who = models.ForeignKey(User, on_delete=models.CASCADE) # person @-ted
    is_shown = models.BooleanField(default=False)
    time_pub = models.DateTimeField(auto_now_add=True)

class Comment_mention(models.Model):
    # 1-m many to a post, 1-m with a comment, 1-m with a user
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    who = models.ForeignKey(User, on_delete=models.CASCADE) # person @-ted
    is_shown = models.BooleanField(default=False)
    time_pub = models.DateTimeField(auto_now_add=True)

# class Notfication(models.Model):
#     #type: atted, followed,
#     who = models.ForeignKey(User, on_delete=models.CASCADE) # person @-ted
#     shot = models.ForeignKey(Shot, on_delete=models.CASCADE, blank=True) 
#     time_pub = models.DateTimeField(auto_now_add=True)