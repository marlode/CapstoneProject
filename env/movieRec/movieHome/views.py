from multiprocessing import context
import re
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import Post
from .forms import RegisterForm, PostForm, SurveyForm
import requests



def movie_rec(request):
    
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            q1 = form.cleaned_data.get("QUESTIONONE") #Director/Actor Preferences\
            q1q1 = form.cleaned_data.get("PERSON_CHOICE") #Name of Person
            q2 = form.cleaned_data.get("QUESTIONTWO") #Mood
            q3 = form.cleaned_data.get("QUESTIONTHREE") #Genre
            q4 = form.cleaned_data.get("QUESTIONFOUR") #Decade Preference
            q5 = form.cleaned_data.get("QUESTIONFIVE") #Rating
            q6 = form.cleaned_data.get("QUESTIONSIX") #Story Setting

            #q4 plus 10 for decade (ex: q4=2000 so q4w10 = 2010 for decade 2000-2010)
            q4w10 = int(q4) + 10
            #q5 plus 2 for rating (ex: q5=0 (1 star) so q5w2 = 2 for voting average between 0 and 2)
            q5w2 = int(q5) + 2


            #Get Genres from MovieDB
            genreRequest = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=e07e6fbbed1779475f88f21defbf334a&language=en-US")
            genre = genreRequest.json()['genres'][int(q3)]['id']

            #Get Person ID from MovieDB, if length of q1q1 is 0 it means there is no preference so a person request isn't necessary
            person = None
            if (len(q1q1) != 0):
                name = str(q1q1).split()
                fName = name[0]
                lName = name[1]
                personRequest = requests.get(f"https://api.themoviedb.org/3/search/person?api_key=e07e6fbbed1779475f88f21defbf334a&language=en-US&query={fName}%20{lName}&page=1&include_adult=false")
                person = personRequest.json()['results'][0]['id']

            #find the 1st movie that best matches all our criteria
            movieRequest = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key=e07e6fbbed1779475f88f21defbf334a&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&primary_release_date.gte={q4}&primary_release_date.lte={q4w10}&vote_average.gte={q5}&vote_average.lte={q5w2}&with_crew={person}&with_genres={genre}&with_watch_monetization_types=flatrate")
            movie = movieRequest.json()['results'][0]

            #Calls a Sentiment-Analysis API and checks Movie Overview for Sentiment
            r = requests.post("https://api.deepai.org/api/sentiment-analysis",
                data={
                    'text': movie['overview'],
                },
                headers={'api-key': 'bce4e272-6788-475b-81df-20d60bc29749'}
            )
            text_sentiment = r.json()
            

            #Movie Poster for Movie Chosen
            imgurl = (f"https://www.themoviedb.org/t/p/w440_and_h660_face/{(movie['poster_path'])}")
           
            context={"data" : [q1,q1q1,q2,q3,q4,q5,q6], "movie": movie, 'imgurl': imgurl, 'text': text_sentiment}

            return render(request,"movie.html", context)
    else:
        form = SurveyForm()

    return render(request, "survey.html", {"form": form})


@login_required(login_url="/login")
def home(request):
    posts = Post.objects.all()

    if request.method == "POST":
        post_id = request.POST.get("post-id")
        user_id = request.POST.get("user-id")

        if post_id:
            post = Post.objects.filter(id=post_id).first()
            if post and (post.author == request.user or request.user.has_perm("main.delete_post")):
                post.delete()
        elif user_id:
            user = User.objects.filter(id=user_id).first()
            if user and request.user.is_staff:
                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except:
                    pass

                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass

    return render(request, 'home.html', {"posts": posts})


@login_required(login_url="/login")
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/home")
    else:
        form = PostForm()

    return render(request, 'create_post.html', {"form": form})


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form": form})