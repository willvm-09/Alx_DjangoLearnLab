from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

urlpatterns = [
    path("api/books", views.BookListAPIView.as_view(), name="book_list_create"),
]

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]