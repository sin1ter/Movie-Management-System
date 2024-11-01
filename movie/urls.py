from django.urls import path
from .views import ( MovieListView, OwnMovieListView, movie_detail, create_movie, 
                    update_movie, delete_movie, rate_movie, report_movie,
                    dashboard, report_list, report_delete, movie_delete)

urlpatterns = [
    path('', MovieListView.as_view(), name='movie_list'), 
    path('own-movies/', OwnMovieListView.as_view(), name='own_movie_list'),
    path('<int:id>/', movie_detail, name='detail_movie'),
    path('create-movie/', create_movie, name='create_movie'), 
    path('update-movie/<int:pk>/', update_movie, name='update_movie'),
    path('delete-movie/<int:pk>/', delete_movie, name='delete_movie'),
    path('<int:movie_id>/rate/', rate_movie, name='rate_movie'),
    path('<int:movie_id>/report/', report_movie, name='report_movie'),

    # Admin
    path('dashboard/', dashboard, name='dashboard'),
    path('report_list/', report_list, name='report_list'),
    path('report_delete/<int:id>/', report_delete, name='report_delete'),
    path('movie-delete/<int:id>/', movie_delete, name='movie_delete')
]