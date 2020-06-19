"""hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from django.conf.urls import url
from hello import settings
from mysite import views
from mysite.models import LikeDislike
from mysite.models import Book
from django.urls import include
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required

app_name = 'ajax'
urlpatterns = [
    path('', views.index, name='index'),
    path('books', views.books, name='books'),
    path('addbook/<int:uid>', views.addbook, name='addbook'),
    #path('addbook', views.addbook, name='addbook'),
    path('enter', views.enter, name='enter'),
    #path('inform', views.inform, name='inform'),
    path('inform/<int:uid>', views.inform, name='inform'),
    path('person', views.person, name='person'),
    path('registration', views.registration, name='registration'),
    path('admin/', admin.site.urls),
    path('inform/<int:pk>/like', views.VotesView.as_view(model=Book, vote_type=LikeDislike.LIKE), name='book_like'),
    path('inform/<int:pk>/dislike', views.VotesView.as_view(model=Book, vote_type=LikeDislike.DISLIKE),
         name='book_dislike'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
