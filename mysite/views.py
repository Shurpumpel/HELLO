from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.contenttypes.models import ContentType
from .models import Persons
from .models import Book
from .models import LikeDislike
import json

class VotesView(View):
    model = None  # Модель данных - Статьи или Комментарии
    vote_type = None  # Тип комментария Like/Dislike

    def post(self, request, pk):
        obj = self.model.objects.get(pk=pk)
        # GenericForeignKey не поддерживает метод get_or_create
        try:
            likedislike = LikeDislike.objects.get(object_id=obj.id)
            if likedislike.vote is not self.vote_type:
                likedislike.vote = self.vote_type
                likedislike.save(update_fields=['vote'])
                result = True
            else:
                likedislike.delete()
                result = False
        except LikeDislike.DoesNotExist:
            obj.votes.create(vote=self.vote_type)
            result = True

        return HttpResponse(
            json.dumps({
                "result": result,
                "like_count": obj.votes.likes().count(),
                "dislike_count": obj.votes.dislikes().count(),
                "sum_rating": obj.votes.sum_rating()
            }),
            content_type="application/json"
        )

def index(request):
    return render(request, "index.html")

def books(request):
    book_list = Book.objects.all()
    return render(request, 'books.html', {'book_list': book_list})

def addbook(request, uid=0):
#def addbook(request):
    person = Persons.objects.get(id=uid)
    if request.method == "POST":
        #person = Persons.objects.get(id=1)
        book = Book()
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.year = request.POST.get("year")
        book.publishing = request.POST.get("publishing")
        book.possibility = request.POST.get("possibility")
        book.wish = request.POST.get("wish")
        book.image = request.POST.get('image')
        book.personid = person
        book.save()
        book_list = Book.objects.filter(personid_id=person)
        return render(request, "person.html", {"book_list": book_list, "person": person})
    else:
        return render(request, "addbook.html")

def enter(request):
    if request.method == "POST":
        login = request.POST.get("login")
        password1 = request.POST.get("password")
        if Persons.objects.filter(phone=login, password=password1).exists():
            person = Persons.objects.get(phone=login, password=password1)
            book_list = Book.objects.filter(personid_id=person)
            return render(request, "person.html", {"person": person, "book_list": book_list})
        else:
            return HttpResponse("Ошибка ввода логина и\или пароля!")
    else:
        return render(request, "enter.html")

#def inform(request):
    #book = Book.objects.get(id=1)
    #person = Persons.objects.get(id=book.personid_id)
    #return render(request, 'inform.html', {"book": book, "person": person})

def inform(request, uid=0):
    book = Book.objects.get(id=uid)
    person = Persons.objects.get(id=book.personid_id)
    return render(request, 'inform.html', {"book": book, "person": person})

def person(request):
    return render(request, "person.html", {"person": person})

def registration(request):
    if request.method == "POST":
        person = Persons()
        person.email = request.POST.get("mail")
        person.password = request.POST.get("password")
        person.surname = request.POST.get("lastname")
        person.name = request.POST.get("name")
        person.phone = request.POST.get("phone")
        person.town = request.POST.get("town")
        person.save()
        return render(request, "person.html", {"person": person})
    else:
        return render(request, "registration.html")

