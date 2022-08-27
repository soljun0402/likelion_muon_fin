from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('musical/<pID>', musical_detail, name="musical"),
    path('musical/like/<pID>', like_product, name="like_product"),
    path('community/<str:id>', detail, name="detail"),
    path('community/', community, name="community"),
    path('community/create/', create, name="create"),
    path('mypage/', mypage, name="mypage"),
    path('musical_list/', musical_list, name="musical_list"),
    path('modify/<str:id>', modify, name="modify"),
    path('delete/<str:id>', delete, name="delete"),
    path('post/scrap/<str:id>', post_scrap, name="post_scrap")
]