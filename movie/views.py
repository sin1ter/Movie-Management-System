from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage

from datetime import timedelta

from .models import Movie, Rating, Report
from accounts.models import User
from .forms import MovieForm, RatingForm, ReportForm

"""
Returns a list of movies
"""
class MovieListView(ListView):
    template_name = 'movie/movie_list.html'
    context_object_name ='movies'
    paginate_by = 10

    def get_queryset(self):
        return Movie.objects.all().order_by('-id')

"""
Returns a list of own movies
"""
class OwnMovieListView(ListView):
    template_name = 'movie/movie_list.html'
    context_object_name ='movies'
    paginate_by = 10
    
    def get_queryset(self):
        return Movie.objects.filter(created_by=self.request.user)
    

"""
Returns a single movie
"""
@login_required
def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    form = RatingForm(request.POST or None) 
    already_reported = Report.objects.filter(user=request.user, movie=movie).exists()
    
    if request.method == 'POST':
        if form.is_valid():
            rating_value = form.cleaned_data['rating']
            already_rated = Rating.objects.filter(user=request.user, movie=movie).first()

            if already_rated:
                already_rated.rating = rating_value
                already_rated.save()
            else:
                Rating.objects.create(user=request.user, movie=movie, rating=rating_value)

            return redirect('detail_movie', id=movie.id)  
    
    return render(request, 'movie/movie_detail.html', {
        'movie': movie,
        'average_rating': movie.average_rating(),
        'total_ratings': movie.total_ratings(),
        'form': form,
        'already_reported': already_reported,
    })

"""
Creates a new movie
"""
@login_required
def create_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)  
            movie.created_by = request.user  
            

            movie.duration_hours = request.POST.get('hours', 0) or 0
            movie.duration_minutes = request.POST.get('minutes', 0) or 0
            movie.duration_seconds = request.POST.get('seconds', 0) or 0
            
            movie.save()  
            return redirect('movie_list')  
        else:
            print(form.errors)  
    else:
        form = MovieForm() 
    
    return render(request, 'movie/create_movie.html', {'form': form})

"""
Updates a movie
"""
@login_required
def update_movie(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            movie = form.save(commit=False)  
            movie.updated_by = request.user
            
            movie.duration_hours = request.POST.get('hours', 0) or 0
            movie.duration_minutes = request.POST.get('minutes', 0) or 0
            movie.duration_seconds = request.POST.get('seconds', 0) or 0
            
            movie.save()
            return redirect('movie_list')
        else:
            print(form.errors)
    else:
        form = MovieForm(instance=movie)

        form.fields['hours'].initial = movie.duration_hours
        form.fields['minutes'].initial = movie.duration_minutes
        form.fields['seconds'].initial = movie.duration_seconds

    return render(request, 'movie/update_movie.html', {'form': form})


"""
Deletes a movie
"""
@login_required
def delete_movie(request, pk):
    movie = Movie.objects.get(pk=pk)
    movie.delete()
    return redirect('movie_list')

@login_required
def rate_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        rating_value = request.POST.get('rating')

        already_rated = Rating.objects.filter(user=request.user, movie=movie).first()

        if already_rated:
            already_rated.rating = rating_value
            already_rated.save()
        else:
            Rating.objects.create(user=request.user, movie=movie, rating=rating_value)
        
        return redirect('movie_detail', movie_id=movie_id)
    
    return render(request, 'movie/movie_detail.html', {'movie': movie})


"""
Handles the report submission of a movie
"""
@login_required
def report_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = Report(
                user=request.user,
                movie=movie,
                reason=form.cleaned_data['reason'],
            )
            report.save()
            return redirect('detail_movie', id=movie_id)
        
    else: 
        form = ReportForm()

    context = {
        'form': form,
        'movie' : movie,
    }

    return render(request, 'movie/report_movie.html', context)


"""
Admin Dashboard
"""
@login_required
def dashboard(request):

    if not request.user.is_staff:
        messages.error(request, "You must be an administrator to view this page.")
        return redirect('movie_list')

    total_movies = Movie.objects.all().count()
    total_users = User.objects.all().count()
    report = Report.objects.all().count()
    
    movies = Movie.objects.all()
    users = User.objects.all()

    movie_paginator = Paginator(movies, 10)
    page_number = request.GET.get('page')
    movie_page_obj = movie_paginator.get_page(page_number)

    users_paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    user_page_obj = users_paginator.get_page(page_number)

    context = {
        'total_movies': total_movies, 
        'total_users': total_users,
        'report': report,
        'movie_page_obj': movie_page_obj,
        'user_page_obj': user_page_obj,
        'movies': movies, 
        'users': users,

    }

    return render(request, 'admin_dashboard.html', context)

""" 
Returns a list of reports
"""
@login_required
def report_list(request):

    if not request.user.is_staff:
        messages.error(request, "You must be an administrator to view this page.")
        return redirect('movie_list')

    reports = Report.objects.all()

    context = {
        'reports': reports,
    }
    return render(request, 'report_list.html', context)


""" 
Handles the report deletion
"""
@login_required
def report_delete(request, id):

    if not request.user.is_staff:
        messages.error(request, "You must be an administrator to view this page.")
        return redirect('movie_list')
    
    report_delete = get_object_or_404(Report, id=id)
    report_delete.delete()
    return redirect('report_list')


""" 
Handles the movie deletion
"""
@login_required
def movie_delete(request, id):
    if not request.user.is_staff:
        messages.error(request, "You must be an administrator to view this page.")
        return redirect('movie_list')
    
    movie_delete = get_object_or_404(Movie, id=id)
    movie_delete.delete()
    return redirect('movie_list')
