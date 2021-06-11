from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import re, bcrypt

# Create your views here.

# beginning of login/register page
def index(request):
    return render(request, 'login.html')

def register(request):
    if request.method == "GET":
        return redirect('/')

    errors = User.objects.validate(request.POST)

    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect("/")

    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']


    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=pw_hash
    )

    request.session['user_id'] = new_user.id
    return redirect("/home")

def login(request):
    if request.method == "GET":
        return redirect('/')

    email =request.POST['email']
    password = request.POST['password']

    if not User.objects.authenticate(email, password):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')

    user = User.objects.get(email=email)
    request.session['user_id'] = user.id
    return redirect("/home")

def logout(request):
    request.session.clear()
    return redirect('/')
# end of login/register page
# ---------------------------------------------------------------------------------

# start of home page
def home(request):
    if 'user_id' not in request.session:
        messages.error(request,'Please Login')
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    posts = Post.objects.all()
    print(posts)
    context = {
        'user':user,
        'posts':posts
    }
    return render(request, "home.html", context)

# create post
def create_post(request):
    posted_by = User.objects.get(id=request.session['user_id'])
    Post.objects.create(
        content = request.POST['content'],
        posted_by = posted_by
    )
    # print('post created:', Post.objects.last().__dict__)
    return redirect("/home")

#Create Comment
def post_comment(request, post_id):
    user = User.objects.get(id=request.session['user_id'])
    post = Post.objects.get(id=post_id)
    Comment.objects.create(
        comment = request.POST['comment'],
        user = user,
        post = post
    )
    print(Comment.objects.last().__dict__)
    return redirect("/home")

# adds like 
def add_like(request,id):
    liked_message = Post.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['user_id'])
    liked_message.user_likes.add(user_liking)
    return redirect("/home")

# adds like to comment
def like(request,id):
    liked_comment = Post.objects.get(id=id)
    comment_liking = User.objects.get(id=request.session['user_id'])
    liked_comment.comment_likes.add(comment_liking)
    return redirect("/home")

# deletes comment
def delete_comment(request,id):
    destroyed = Comment.objects.get(id=id)
    destroyed.delete()
    return redirect('/home')

# deletes post
def delete_post(request,id):
    remove = Post.objects.get(id=id)
    remove.delete()
    return redirect('/home')

# end of home page
# ----------------------------------------------------------------------------------------

def food(request):
    if 'user_id' not in request.session:
        messages.error(request,'Please Login')
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    foods = Food.objects.all()
    print(foods)
    context = {
        'user':user,
        'foods':foods
    }
    return render(request,'food.html',context)

# create food
def create_food(request):
    Food.objects.create(
        origin_food = request.POST['origin_food'],
        appetizer = request.POST['appetizer'],
        main_course = request.POST['main_course'],
        dessert = request.POST['dessert']
    )
    return redirect('/home')

# post food on home page
def post_food(request,food_id):
    user = User.objects.get(id=request.session['user_id'])
    foods = Food.objects.get(id=food_id)
    Food.objects.create(
        foods = request.POST['foods'],
        user = user,
        food = foods
    )
    print(Food.objects.last().__dict__)
    return redirect('/home')

# edit food
def edit(request, food_id):
    food_id = Food.objects.get(id=food_id)
    context = {
        'food': food_id
    }
    return render(request, 'food.html', context)

# update food
def update(request, food_id):
    errors = Food.objects.validate(request.POST)
    if errors:
        for (key, value) in errors.items():
            messages.error(request, value)
        return redirect(f'/food/{food_id}/edit')
    to_update = Food.objects.get(id=food_id)
    to_update.origin_food = request.POST['origin_food']
    to_update.appetizer = request.POST['appetizer']
    to_update.main_course = request.POST['main_course']
    to_update.dessert = request.POST['dessert']
    to_update.save()

    return redirect('/home')


