from cgitb import text
from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from .models import Post
from .forms import RegisterForm, PostForm, SurveyForm
import requests

def get_movie (q1,q1name,q2,q3,q4,q5,q6):

    arr = [q3,q4,q5,q6]
   
    for item in arr:
        if (item == 'No Preference'):
            item = ''

    #The variables below are used for the API call to create a range between two numbers
    #q4 plus 10 for decade (ex: q4=2000 so q4w10 = 2010 for decade 2000-2010)
    if (q4 == ''):
        q4w10 = int(q4) + 10
    else:
        q4w10 = ''

    if(q5 == ''):
    #q5 plus 2 for rating (ex: q5=0 (1 star) so q5w2 = 2 for voting average between 0 and 2)
        q5w2 = int(q5) + 2
    else:
        q5w2 = ''

    #Get Genres from MovieDB and the id that matches the genre specified by the user
    if(q3 == ''):
        genreRequest = requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=e07e6fbbed1779475f88f21defbf334a&language=en-US")
        genre = genreRequest.json()['genres'][int(q3)]['id']
    else:
        genre = ''

    #Get Person ID from MovieDB, if length of q1q1 is 0 it means there is no preference so a person request isn't necessary
    person = None
    if (len(q1name) != 0):
        name = str(q1name).split()
        fName = name[0]
        lName = name[1]
        personRequest = requests.get(f"https://api.themoviedb.org/3/search/person?api_key=e07e6fbbed1779475f88f21defbf334a&language=en-US&query={fName}%20{lName}&page=1&include_adult=false")
        person = personRequest.json()['results'][0]['id']

    #call movie api for keyword ids based on question 6 and pick first id
    if(q6 == ''):
        keywordRequest = requests.get(f"https://api.themoviedb.org/3/search/keyword?api_key=e07e6fbbed1779475f88f21defbf334a&query={q6}&page=1")
        keyword_id = keywordRequest.json()['results'][0]['id']
    else:
        keyword_id = ''

    #find the 1st movie that best matches all our criteria

    url = f"https://api.themoviedb.org/3/discover/movie?api_key=e07e6fbbed1779475f88f21defbf334a&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_keywords={keyword_id}&primary_release_date.gte={q4}&primary_release_date.lte={q4w10}&vote_average.gte={q5}&vote_average.lte={q5w2}&with_crew={person}&with_genres={genre}&with_watch_monetization_types=flatrate"
    movieRequest = requests.get(url)
    movie_from_api = None

    #in case the api is unable to find a movie based on all the criteria specified by the user, we return a movie with 3 out of the 6 criteria omitted, otherwise get 1st movie result
    if not movieRequest.json()['results']:
        url = f"https://api.themoviedb.org/3/discover/movie?api_key=e07e6fbbed1779475f88f21defbf334a&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_keywords={keyword_id}&with_genres={genre}&with_watch_monetization_types=flatrate"
        movieRequest = requests.get(url)
        movie_from_api = movieRequest.json()['results'][0]
    else:
        movie_from_api = movieRequest.json()['results'][0]


    #Function defined to call a Sentiment-Analysis API and checks Movie Overview for Sentiment
    def call_sentiment(movie):
        r = requests.post("https://api.deepai.org/api/sentiment-analysis",
            data={
                'text': movie['overview'],
            },
            headers={'api-key': 'bce4e272-6788-475b-81df-20d60bc29749'}
        )
        text_sentiment_value = r.json()['output'][0]
        return text_sentiment_value

    #Below the loop continuously searches for a match between movie overview sentiment and the sentiment specified by the user
    #The loop continues searching each result and every page, breaking only when it reaches the final result with no match or finds a match
    
    i = 0
    j = 1
    tsv = call_sentiment(movie_from_api)
    compare_sentiments = (tsv == q2)
    while(compare_sentiments == False):

        results_length     = len(movieRequest.json()['results'])-1
        i                  += 1
        movie_from_api     = movieRequest.json()['results'][i]
        tsv                = call_sentiment(movie_from_api)
        compare_sentiments = (tsv == q2)     

        if (i == results_length and movieRequest.json()['total_pages'] > j):
            j            += 1
            i            = 0
            movieRequest = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key=e07e6fbbed1779475f88f21defbf334a&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page={j}&primary_release_date.gte={q4}&primary_release_date.lte={q4w10}&vote_average.gte={q5}&vote_average.lte={q5w2}&with_crew={person}&with_genres={genre}&with_watch_monetization_types=flatrate")
            url          = f"https://api.themoviedb.org/3/discover/movie?api_key=e07e6fbbed1779475f88f21defbf334a&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page={j}&primary_release_date.gte={q4}&primary_release_date.lte={q4w10}&vote_average.gte={q5}&vote_average.lte={q5w2}&with_crew={person}&with_genres={genre}&with_watch_monetization_types=flatrate"

        elif(i == results_length and movieRequest.json()['total_pages'] == j):
            break

    
    #Movie Poster for Movie Chosen
    poster = (f"https://www.themoviedb.org/t/p/original/{(movie_from_api['poster_path'])}")
    backdrop = (f"https://www.themoviedb.org/t/p/original/{(movie_from_api['backdrop_path'])}")
    context={"data" : [q1,q1name,q2,q3,q4,q5,q6], 'imgurl': poster, 'movie': movie_from_api, 'overview': movie_from_api['overview'], 'title': movie_from_api['original_title'], 'backdrop': backdrop}
    return context


def survey(request):
    

    if request.method == 'POST':
        form = SurveyForm(request.POST)

        if form.is_valid():

            q1 = form.cleaned_data.get("QUESTIONONE") #Director/Actor Preferences\
            q1name = form.cleaned_data.get("PERSON_CHOICE") #Name of Person
            q2 = form.cleaned_data.get("QUESTIONTWO") #Mood
            q3 = form.cleaned_data.get("QUESTIONTHREE") #Genre
            q4 = form.cleaned_data.get("QUESTIONFOUR") #Decade Preference
            q5 = form.cleaned_data.get("QUESTIONFIVE") #Rating
            q6 = form.cleaned_data.get("QUESTIONSIX") #Story Setting

            context = get_movie(q1,q1name,q2,q3,q4,q5,q6)


            return render(request, 'movie.html', context)
        else:
            pass
    else:
        form = SurveyForm()

    return render(request, "survey.html", {"form": form})

@login_required(login_url="/login")
def home(request):

    url = f"https://api.themoviedb.org/3/discover/movie?api_key=e07e6fbbed1779475f88f21defbf334a&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_watch_monetization_types=flatrate"
    movieRequest = requests.get(url)
    movie_from_api = movieRequest.json()['results'][0]
    imgurl = (f"https://www.themoviedb.org/t/p/original/{(movie_from_api['backdrop_path'])}")

    context = {'posts': Post.objects.all(), 'backdrop': imgurl, 'movie': movie_from_api, 'overview': movie_from_api['overview'], 'title': movie_from_api['original_title']}

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

    return render(request, 'home.html', context)


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