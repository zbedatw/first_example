from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.transaction import commit
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.functional import empty
from django.http import JsonResponse

from .forms import EditReview
from .models import Movie, Review
from . import forms


def movie_list(request):
    movies = Movie.objects.all().order_by('year')
    return render(request, 'movies/movie_list.html', {'movies':movies})


def movie_detail(request, id):
   movie = Movie.objects.get(id=id)
   reviews = movie.reviews.all()
   user_review = empty
   if request.user.is_authenticated:
        user_review = movie.reviews.filter(user=request.user).first()
   rating_range = range(1, 6)
   return render(request, "movies/movie_detail.html",
        {'movie':movie,'reviews':reviews,'rating_range': rating_range, 'user_review':user_review})



@login_required(login_url="/accounts/login")
def movie_create_review(request, id):
    movie = Movie.objects.get(id=id)
    if request.user.is_authenticated:
        if movie.reviews.filter(user=request.user).first():
           return redirect('movies:detail', id=id)
    if request.method == "POST":
        form = forms.CreateReview(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.movie_id = movie.id
            instance.save()
            return JsonResponse({'success': True, 'redirect_url': reverse('movies:detail', args=[movie.id])})
    else:
        form = forms.CreateReview()
    return render(request, "movies/movie_create_review.html", {'form': form, 'movie': movie})


def get_embed_url(youtube_url):
    if "youtube.com/watch?v=" in youtube_url:
        video_id = youtube_url.split("v=")[-1]
        return f"https://www.youtube.com/embed/{video_id}"
    return youtube_url  # Return original if not a YouTube link


from django.http import JsonResponse


def movie_edit_review(request, id):
    movie = Movie.objects.get(id=id)
    review = movie.reviews.filter(user=request.user).first()
    if not review:
        return redirect('movies:detail', id=movie.id)  # Handle case where user has no review

    if request.method == 'POST':
        form = forms.EditReview(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()  # Save the updated review
            return JsonResponse({'success': True, 'redirect_url': reverse('movies:detail', args=[movie.id])})
    else:
        form = forms.EditReview(instance=review)

    return render(request, 'movies/movie_edit_review.html', {'form': form, 'review': review})

def movie_delete_review(request, review_id,id):
    # Ensure that the method is DELETE
    if request.method == 'DELETE':
        review = get_object_or_404(Review, id=review_id, user=request.user)
        review.delete()
        return JsonResponse({'success': True, 'redirect_url': reverse('movies:detail', args=[id])})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)