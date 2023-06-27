from django.db import IntegrityError
from django.shortcuts import render, reverse, redirect
from .models import Shot, Hashtag, Mention, UserProfile, Comment
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

def index(request):
    shots = Shot.objects.order_by("-time_pub")
    context = {'shots': shots}
    return render(request, 'headshot/home_page.html', context)

def popular(request):
    shots = Shot.objects.annotate(numoflikers=Count('likers')).order_by('-numoflikers')[:5]
    context = {'shots':shots}
    return render(request, 'headshot/popular.html', context)

def profile_page(request):
    userprofile = UserProfile.objects.get(user=request.user)
    return render(request, 'headshot/profile_page.html', {'userprofile':userprofile})

def test(request):
    shots = Shot.objects.order_by("-time_pub")
    context = {'shots': shots}
    return render(request, 'headshot/test.html', context)

def loginsignup(request):
    return render(request, 'headshot/loginsignup.html')

def post(request):
    return render(request, 'headshot/post.html')

def signup(request):
    username = request.POST['username']
    password = request.POST['password']
    user_pfp = request.FILES['user_pfp']
    try:
        user = User.objects.create_user(username=username, password=password)
    except IntegrityError: 
        messages.add_message(request, messages.ERROR, "This username has already been taken")
        return HttpResponseRedirect(reverse('shot:loginsignup')) 
    if user is not None:
        userp = UserProfile(user=user, user_pfp=user_pfp)
        userp.save()
        login(request, user)
        return redirect("shot:index")
    else: 
        return HttpResponseRedirect(reverse('shot:loginsignup')) 


def logon(request):
    try:
        username = request.POST['username'] 
        password = request.POST['password']

    except:
        return HttpResponseRedirect(reverse('shot:loginsignup')) 
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect("shot:index")
    else:
        return HttpResponseRedirect(reverse('shot:loginsignup')) 

def log_out(request):
    logout(request)
    return redirect('shot:loginsignup')

def like(request, shot_id):
    shot = Shot.objects.get(id=shot_id)
    shot.likers.add(request.user)
    return redirect(request.META['HTTP_REFERER'])

def unlike(request, shot_id):
    shot = Shot.objects.get(id=shot_id)
    shot.likers.remove(request.user)
    return redirect(request.META['HTTP_REFERER'])

def follow(request, author_id ):    
    celeb = UserProfile.objects.get(user=User.objects.get(id=author_id))
    celeb.followers.add(request.user)
    return redirect(request.META['HTTP_REFERER'])

def unfollow(request, author_id):
    celeb = UserProfile.objects.get(user=User.objects.get(id=author_id))
    celeb.followers.remove(request.user)
    return redirect(request.META['HTTP_REFERER'])

def post_comment(request, shot_id):
    if request.method == 'POST':
        comment_text = request.POST['comment_text']
        comment_pic = request.FILES['comment_pic']
        shot = Shot.objects.get(id=shot_id)
        comment = Comment(comment_pic=comment_pic, comment_text=comment_text, comment_author=request.user, shot=shot)
        comment.save()

        post_hashtag_mention(comment_text, shot)
        return redirect(request.META['HTTP_REFERER'])
         
    else:
        shot = Shot.objects.get(id=shot_id)
        context = {'shot':shot, 'comments':Comment.objects.filter(shot=shot)}
        return render(request, 'headshot/comment.html', context)

def author(request,author_id):
    user = User.objects.get(id=author_id)
    userprofile  = UserProfile.objects.get(user=user)
    context = {'author':user, 'authorprofile':userprofile, 'shots':Shot.objects.filter(author=user)}
    return render(request, 'headshot/user.html', context)


def hashtag(request, hashtag_text):
    try:
        hashtag = Hashtag.objects.get(hashtag_text=hashtag_text)
    except:
        return redirect('shot:index')
    context = {'shot': hashtag_text, 'shots':hashtag.shots.all()}
    print(context)
    return render(request, 'headshot/hashtag.html', context)

def mention(request, mention_text):
    try:
        who = User.objects.get(username=mention_text[1:])
        mentions = Mention.objects.filter(who=who)
        shots = []
        for mention in mentions:
            shots.append(mention.shot)
    except:
        return redirect('shot:index')
    context = {'shot': mention_text, 'shots':shots}
    return render(request, 'headshot/mention.html', context)

def post_hashtag_mention(text, shot):
    words = text.split()
    print(words)

    for word in words:
        if word and word[0] == "#":
            try:
                hashtag = Hashtag.objects.get(hashtag_text=word.strip().lower())
            except ObjectDoesNotExist:
                hashtag = Hashtag(hashtag_text=word.lower().strip())
                hashtag.save()
           
            hashtag.shots.add(shot)

        elif word and word[0] == "@":
            user = User.objects.get(username=word[1:])
            print(f'Posting. @{user.username}')

            mention = Mention(shot=shot, who=user)
            try:
                mention.save()
            except:
                pass

def post_shot(request):
    if request.method == 'POST':
        shot_text = request.POST['shot_text']
        shot_pic = request.FILES['shot_pic']
        shot = Shot(shot_pic=shot_pic, shot_text=shot_text, author=request.user)
        shot.save()

        post_hashtag_mention(shot_text, shot)
        return redirect(request.META['HTTP_REFERER'])
         
    else:
        return redirect(request.META['HTTP_REFERER'])

def delete(request, shot_id):
    shot = Shot.objects.get(id=shot_id)
    shot.delete()
    return redirect(request.META['HTTP_REFERER'])

def search(request):
    tag_text = request.GET.get('search', '').strip().lower()
    if tag_text[0] == '@':
        return HttpResponseRedirect(reverse('shot:mention', args=(tag_text, ))) 
    elif tag_text[0] == '#':
        return HttpResponseRedirect(reverse('shot:hashtag', args=(tag_text, )))
    else:
        tag_text = "#"+tag_text
        return HttpResponseRedirect(reverse('shot:hashtag', args=(tag_text, )))

def like_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.likers_comment.add(request.user)
    return redirect(request.META['HTTP_REFERER'])

def unlike_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.likers_comment.remove(request.user)
    return redirect(request.META['HTTP_REFERER'])

def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return redirect(request.META['HTTP_REFERER'])
