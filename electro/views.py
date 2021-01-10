import random
from django.shortcuts import redirect, render

# Create your views here.
def home(request):
    top = random.randrange(5, 25)  #generer entre 5 et 10 voitures sur les voies
    top_n = [random.randrange(0,3) for i in range(0, top)]
    bottom = random.randrange(5, 25)
    bottom_n = [random.randrange(0,3) for i in range(0, bottom)]
    left = random.randrange(5, 25)
    left_n = [random.randrange(0,3) for i in range(0, left)]
    right = random.randrange(5, 25)
    right_n = [random.randrange(0,3) for i in range(0, right)]
    print(top, bottom, left, right)
    context = {
        'top_n': top_n,
        'bottom_n': bottom_n,
        'left_n': left_n,
        'right_n': right_n
    }
    return render(request, 'home.html', context)

def index(request):
    return render(request, 'index.html')

def docs(request):
    return render(request, 'docs.html')

def root(request):
    return redirect('/index')