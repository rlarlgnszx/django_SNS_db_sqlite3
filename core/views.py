

from django.shortcuts import render , redirect
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.models import User, auth 
from django.contrib import messages
from .models import FollowerCount, LikePost, Profile ,Post , Comment
from django.contrib.auth.decorators import login_required
from itertools import chain
import random
@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)


    user_following_list = [request.user.username]
    feed = [] 

    user_following = FollowerCount.objects.filter(follower = request.user.username)
    for user in user_following:
        user_following_list.append(user.user)
    
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)
    # print(feed)
    #! Post가 들어있는 리스트를 chain 으로 묶어서 더해줄수가 있다.
    feed_list = list(chain(*feed))
    #! 객체 정렬하는 방법 .
    feed_list = sorted(feed_list, key=lambda x:x.created_at)
    comment  = dict()
    # print(feed_list)
    for feed in feed_list:
        
        comment[feed.id] = Comment.objects.filter(post_id=feed.id)
        # print(feed.comments[0].user_profileimg[0].profileimg.url)
        # print("next")

    ##* user suggestion starts
    all_users = User.objects.all()
    user_following_all=[]
    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
    new_suggestion_list = [x for x in list(all_users) if (x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)

    final_suggestions_list = [x for x in list(new_suggestion_list) if (x not in list(current_user))]
    random.shuffle(final_suggestions_list)

    username_profile = []
    username_profile_list = []

    for users in final_suggestions_list:
       
        username_profile.append(users.id)
    for id in username_profile:
        profile_lists = Profile.objects.filter(id_user =id)
        username_profile_list.append(profile_lists)

    suggestion_username_profile_list = list(chain(*username_profile_list))
    return render(request,'index.html',{'user_profile':user_profile,'posts':feed_list ,'suggestion_username_profile_list':suggestion_username_profile_list[:4]})

@login_required(login_url='signin')
def comment(request):
    if request.method=="POST":
        recomment = request.POST['recomment']
        post_id = request.POST['post_id']
        username=request.POST['user_id']
        post=Post.objects.get(id=post_id)
        #! objects.get 과 filter의 차이점 중시!
        new_like = Comment.objects.create(post_id =post_id,user_id=username,comment=recomment)
        new_like.save()
        
        return  redirect("/")


@login_required(login_url='signin')
def delete(request):
    print("##############################")
    if request.method == "POST":
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@")
        delete_id = request.POST['post_id']
        delete_post = Post.objects.filter(id=delete_id).first()
        print("i delete POST :" ,delete_post)
        delete_post.delete()
        return redirect("/")
    else:
        return redirect("/")

def signup(request):

    if request.method =="POST":
        username =request.POST['username']
        email =request.POST['email']
        password =request.POST['password']
        password2 = request.POST['password2']

        if password2 ==password:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email , password=password)
                user.save()
                

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request,user_login)
                #create Profile object to new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('setting')

        else:
            messages.info(request,"Password Not Matching")
            return redirect('signup')
            

    else:
        return render(request,'signup.html')


def singin(request):

    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("/")
        else:
            messages.info(request,"Credentials Invalid")
            return redirect("signin");


    else:
        return render(request,'signin.html')
def logout(request):
    auth.logout(request)
    return  redirect("signin")
def setting(request):

    print(request.user)
    user_profile = Profile.objects.get(user=request.user)

    if request.method=="POST":
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
        else:
            image = request.FILES.get('image')
        user_profile.profileimg = image
        user_profile.bio = request.POST['bio']
        user_profile.location = request.POST['location']
        user_profile.save()
        return redirect('setting')
    return render(request,'setting.html',{'user_profile':user_profile})
@login_required(login_url="signin")
def upload(request):
    if request.method=="POST":
        user = request.user.username
        image= request.FILES.get('image_upload')
        caption=request.POST['caption']

        new_post = Post.objects.create(user=user,image=image,caption=caption)
        new_post.save()
        return redirect("/")
    else:
        return redirect("/")
    return HttpResponse("HELLO")


@login_required(login_url="signin")
def profile(request,pk):
    user_object = User.objects.get(username=pk)
    user_profile= Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_len = len(user_posts)
    follower = request.user.username
    user = pk



    if FollowerCount.objects.filter(follower=follower,user=user).first():
        button_text= "Unfollow"
    else:
        button_text = "Follow";
    user_follower = len(FollowerCount.objects.filter(user=pk));
    user_following = len(FollowerCount.objects.filter(follower=pk));



    context = {
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_post_len':user_post_len,
        'button_text':button_text,
        'user_followers':user_follower,
        'user_followings':user_following,
    }

    return render(request,'profile.html',context)

@login_required(login_url="signin")
def like(request):
    username=request.user.username
    post_id= request.GET.get('post_id')
    
    post=Post.objects.get(id=post_id)
    #! objects.get 과 filter의 차이점 중시!
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()
    if like_filter ==None:
        new_like = LikePost.objects.create(post_id =post_id,username=username)
        new_like.save()
        post.no_of_likes +=1
        post.save()
        return  redirect("/")
    else:
        like_filter.delete()
        post.no_of_likes -=1
        post.save()
        return redirect("/")

@login_required(login_url='signin')
def follow(request):
    if request.method=="POST":
        follower = request.POST['follower']
        user = request.POST['user']
        try:
            rehome = request.POST['home']
            if FollowerCount.objects.filter(follower=follower,user=user).first():
                delete_follower = FollowerCount.objects.get(follower=follower,user=user)
                delete_follower.delete()
                print(follower ,"unfollow ", user)

                return redirect("/")
            else:
                new_follower =  FollowerCount.objects.create(follower=follower,user=user)
                print(follower ,"follow ", user)
                new_follower.save()
                return redirect("/")
        except:
            if FollowerCount.objects.filter(follower=follower,user=user).first():
                delete_follower = FollowerCount.objects.get(follower=follower,user=user)
                delete_follower.delete()
                print(follower ,"unfollow ", user)

                return redirect("/profile/"+user)
            else:
                new_follower =  FollowerCount.objects.create(follower=follower,user=user)
                print(follower ,"follow ", user)
                new_follower.save()
                return redirect("/profile/"+user)
    else:
        return redirect("/")


def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    if request.method=="POST":
        username=  request.POST['username']
        user_object = User.objects.filter(username__icontains  =username)#! username을 포함하는 모든 object 반환

        username_profile = []
        username_profile_list  =[]

        for users in user_object:
            username_profile.append(users.id)
        for id in username_profile:
            profile_list = Profile.objects.filter(id_user=id)
            username_profile_list.append(profile_list)
        
        username_profile_list = list(chain(*username_profile_list))

    return render(request,'search.html',{'username_profile_list':username_profile_list,'username_profile':user_profile})
