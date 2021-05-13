from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django import forms
from .models import Afiliado, Period
from .uploading_data import handle_uploaded_file, download_file
import mimetypes
import os
from .utils import get_plot, get_plot_bar
from .create_reports import stats_by_state, stats_historic, stats_state_and_period, stats_bad_by_state

# Django form in charge of looking for the person in the database
class AfiliadoLookUpForm(forms.Form):
    documment_number = forms.IntegerField(label="", widget= forms.TextInput(attrs={'class' : 'login_test'}))

class FileForm(forms.Form):
    file = forms.FileField()
# Create your views here.


def upload_file(request):
    if request.method == "POST":
        form = FileForm(request.POST, request.FILES)
        if form.is_valid and 'file' in request.FILES:
            handle_uploaded_file(request.FILES['file'])
            return render(request, "users/upload_data.html", {
                "message": "Archivo subido correctamente"
                })
    else:
        form = FileForm()
    return render(request, "users/upload_data.html", {
        'form': form
    })


def download(request):
    return download_file()


def executive_view(request):
    """
    View that the executive of the company can see
    """
    # download_file()
    if request.user.is_authenticated:
        # show the amount of people that are in each of the states
        values_state, labels_state = stats_by_state()
        periods, amount_people = stats_historic()
        values_historic, labels_historic = stats_state_and_period()
        # the second pie chart
        values_bad_people = stats_bad_by_state()
        return render(request, "users/executive.html", {
            'pie_value_state': values_state,
            'pie_label_state': labels_state,
            'bar_periods': periods,
            'values_people': amount_people,
            'bar_historic_labels': values_historic,
            'bar_historic_values': labels_historic,
            'pie_bad_people': values_bad_people
        })
    else:
        return render(request, "us expectedcss(css-rparentexpected)ers/error_not.html") 


def index(request):
    # currently signed user

    # add the three posible cases in which the website should show difference


    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    if request.user.username == "foo":
        if request.method == "POST":
            look_text = request.POST["look_doc"]
            if look_text is not None and look_text != "":
                # if it is not none 
                val = Afiliado.objects.filter(document_number=look_text)
                if val.exists():
                    return render(request, "users/user.html", {
                    "person": Afiliado.objects.get(document_number=look_text),
                     })
                else:
                    return render(request, "users/user.html", {
                    "not_found": True,
                     })

        else:

            return render(request, "users/user.html", {
                "form": AfiliadoLookUpForm()
                })
    elif request.user.username == "admin":
        return HttpResponseRedirect(reverse("upload_file"))
    elif request.user.username == "ejecutivo":
        return HttpResponseRedirect(reverse("executive"))

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid credentials"
            })
    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/login.html")