from django.urls import path
from menu_app.views import MenuView

app_name = "menu_app"


urlpatterns = [
    path('', MenuView.as_view(), name='main_menu'),
    path('<path:url_item>/', MenuView.as_view(), name='child_menu'),
]
