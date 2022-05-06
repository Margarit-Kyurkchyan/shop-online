from django.urls import path
from .views import ProductList, PhotoList, ProductDetail, PhotoDetail, CategoryDetail

urlpatterns = [
    # path('<int>')
    path('', ProductList.as_view()),
    path('<int:pk>', ProductDetail.as_view()),
    path('photo', PhotoList.as_view()),
    path('photo/<int:pk>', PhotoDetail.as_view()),
    path('category/<int:pk>', CategoryDetail.as_view()),
]