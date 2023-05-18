"""importing modules"""
from django.shortcuts import render

# Create your views here.


def home(request):
    """Home"""
    return render(request, "index.html")





def base(request):
    """Home"""
    return render(request, "base.html")

# def donor(request):
#     """Home"""
#     return render(request, "donordetails.html")



