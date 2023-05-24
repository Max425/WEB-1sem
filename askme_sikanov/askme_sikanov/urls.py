from django.contrib import admin
from django.urls import path
from askme import views
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('admin/', admin.site.urls),
    path('question/<int:question_id>/', views.question, name="question"),
    path('ask/', views.ask, name="ask"),
    path('logout/', views.logout_view, name="logout"),
    path('login/', views.login_view, name="login"),
    path('settings/', views.settings, name="settings"),
    path('signup/', views.signup, name="signup"),
    path('tag/<str:tag_name>/', views.tag, name="tag"),
    path('hot/', views.hot, name="hot"),
    path('vote_up/', views.vote_up, name="vote_up"),
    path('is_correct/', views.is_correct, name="is_correct"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)