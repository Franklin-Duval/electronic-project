import random
from django.shortcuts import redirect, render
from django.http import Http404
from django.http import JsonResponse,HttpResponse
from .brain import brain
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from background_task import background
import time
import threading


t = None
threadForUpdatingState=None
voie1=0

@background
def do_something():
    print("I'm a background ")



def update_state_lights(traffic_light,color):
    # change l'etat des leds
    for el in traffic_light[color]:
        GPIO.output(traffic_light[el],GPIO.LOW)
    GPIO.output(traffic_light[color],GPIO.HIGH)


def background_process():
    #cette fonction permet d'ecouter les capteurs ultrasons
    global voie1
    t=threading.currentThread()
    while getattr(t,"do_run",True):
        print("process started")
        voie1+=1
        print(voie1)
        time.sleep(3)
        print("process finished")
        
        #GPIO.output(GPIO_TRIGGER, True)
     
        # set Trigger after 0.01ms to LOW
        #time.sleep(0.00001)
        #GPIO.output(GPIO_TRIGGER, False)
     
        #StartTime = time.time()
        #StopTime = time.time()
     
        # save StartTime
        #while GPIO.input(GPIO_ECHO) == 0:
        #    StartTime = time.time()
     
        # save time of arrival
        #while GPIO.input(GPIO_ECHO) == 1:
        #    StopTime = time.time()
     
        # time difference between start and arrival
        #TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        #distance = (TimeElapsed * 34300) / 2
    print("stopped")

def index(request):
    #lance la simulation
    global t
    if t==None or not t.is_alive():
        print("start threading")
        t=threading.Thread(target=background_process, args=(), kwargs={})
        t.setDaemon(True)
        t.start()
    return HttpResponse("main thread content")

def deactive(request):
    #arrete la simulation
    global t
    global voie1
    t.do_run=False
    t.join()
    return HttpResponse(f"finished, result={voie1}")


@csrf_exempt
def compute_time_send_response(request):
    # compute the time needed and return the green time
    cars1=int(request.POST['cars1'][0])
    cars2=int(request.POST['cars2'][0])
    return JsonResponse({"result":brain(cars1,cars2)}, safe=False)


def set_light(traffic_light,color):
    return

# Create your views here.
def home(request):
    #genere de facon aleatoire les voitures sur chaque voie
    top = random.randrange(5, 10)  #generer entre 5 et 10 voitures sur les voies
    top_n = [random.randrange(0,3) for i in range(0, top)]
    bottom = random.randrange(5, 10)
    bottom_n = [random.randrange(0,3) for i in range(0, bottom)]
    left = random.randrange(5, 10)
    left_n = [random.randrange(0,3) for i in range(0, left)]
    right = random.randrange(5, 10)
    right_n = [random.randrange(0,3) for i in range(0, right)]
    print(top_n, bottom_n, left, right)
    context = {
        }