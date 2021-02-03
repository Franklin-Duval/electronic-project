import random
from django.shortcuts import redirect, render
from django.http import Http404
from django.http import JsonResponse,HttpResponse
from .brain import brain
from django.views.decorators.csrf import csrf_exempt
import time
import threading
import RPi.GPIO as GPIO
from gpiozero import DistanceSensor # detecteur de distance
import sys
import json

GPIO.setmode(GPIO.BOARD)

GPIO_TRIGGER = 16
GPIO_ECHO = 18

nb_voie=0
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


########################################################

#                FONCTIONNEMENT

########################################################

# dans la fonction background, on ecoute les capteurs dans le cas nominal et on envoie des posts vers le front
# dans le cas de simulation, on poste vers le front mais le front repond immediatement, avec les nouvelles informations 
# fournies par le simulateur


# le feu est organisé comme suit [vert,jaune,rouge] donc les indices sont 0,1,2 respectivement

#####################################################

#               DECLARATION

#####################################################
t=None
threadForUpdatingState=None
transitions=[0,1,2,2] #l'etat initial de deux feux est 0 et pour les deux autres c'est 2, le contenu du tableau est les indices des feux alumes

#contient les numero de toutes les leds, numerotees de 1 à 4 dans cet ordre et les feux du vert au rouge CE TABLEAU NE DOIT JAMAIS CHANGER
# exple : LEDS=[(23,4,5),(5,4,1),(6,4,6),(13,3,5)]
# qui veut dire que le feu 1 est constitué des leds aux pins 23,4,5


#######################################################

#                   CLASSE UTILITAIRE

#######################################################

class TrafficController():
    def __init__(self,leds,sensors=[],nb=2):
        self.nb=nb
        self.leds=leds
        self.state_phase1=0
        self.state_phase2=2
        #enregistrement des voies
        self.voie={}
        for i,led in enumerate(self.leds):
            self.voie[i]=0
            GPIO.setup(led,GPIO.OUT)
            
        # enregistrement des senseurs
        self.sensors=sensors
        print(f"LES SENSEURS - {self.sensors}")

    def all_off(self):
        #eteint tout le monde
        for light in self.leds:
            for led in light:
                GPIO.output(led,GPIO.LOW)

    def all_on(self):
        #allume tout le monde
        for light in self.leds:
            for led in light:
                GPIO.output(led,GPIO.HIGH)

    def set_led_on(self,index_feu,index_led):
        #allume une led precise sur un feu
        assert index_led>=0 and index_led<3 and index_feu>=0 and index_feu<2
        for led in self.leds[index_feu]:
            print(f"Eteindre sur le feu {index_feu} la led numero {led} ")
            GPIO.output(led,GPIO.LOW)
        print(f"Allumer sur le feu {index_feu} la led numero {index_led} ")
        GPIO.output(self.leds[index_feu][index_led],GPIO.HIGH)#ce qu'on veut vraiment alumer
    


    def distance(self,trigger,echo):
        # set Trigger to HIGH
        GPIO.output(trigger, True)
    
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(trigger, False)
    
        StartTime = time.time()
        StopTime = time.time()
    
        # save StartTime
        while GPIO.input(echo) == 0:
            StartTime = time.time()
    
        # save time of arrival
        while GPIO.input(echo) == 1:
            StopTime = time.time()
    
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
    
        return distance
    def listen(self):
        global nb_voie
        dist_voie1=0.2
        dist_voie2=0.5
        car_entrance=False
        car_outance=False
        #cette fonction permet d'ecouter les capteurs ultrasons et mettre a jour les variables 
        t=threading.currentThread() 
        while getattr(t,"do_run",True):
            dist1 = self.distance(16,18)
            dist2 = self.distance ()

            # incrementer les voitures
            if (dist1<20) and not car_entrance:
                car_entrance=True
                nb_voie+=1
                print(f"le nombre de voitures est {nb_voie}")
            if (dist1>=20):
                car_entrance=False

            
            #decrementer les voitures
            if (dist2<20) and not car_outance:
                car_outance=True
                nb_voie-=1
                print(f"le nombre de voitures est {nb_voie}")
            if (dist2>=20):
                car_outance=False
            time.sleep(0.5)
    
    def set_phase1_on(self,led_state):
        #allume une led precise des deux feux d'une phase
        self.set_led_on(0,led_state)


    def set_phase2_on(self,led_state):
        #allume une led precise des deux feux de l'autre
        self.set_led_on(1,led_state)



    def switch_state(self):
        #allume les leds en suivant les transitions
        self.state_phase1=(self.state_phase1+1)%4
        self.state_phase2=(self.state_phase2+1)%4
        self.set_phase1_on(transitions[self.state_phase1])
        self.set_phase2_on(transitions[self.state_phase2])
        


#declaration

AllMightyController=TrafficController(leds=[(7,5,3),(15,13,11)],sensors=((16,18),(None,None)))
#AllMightyController.set_led_on(1,1)
#AllMightyController.switch_state()

##############################################################################

#                                  VIEWS

############################################################################


# Create your views here.
def home(request):
    AllMightyController.switch_state()
    return HttpResponse("You are at Home!")



@csrf_exempt
def compute_time_send_response(request):
    # compute the time needed and return the green time
    print(" request body ",request.body)
    temps_vert=0
    try:
        data=json.loads(request.body.decode("utf-8"))
        print(data)
        cars1=int(data['north'])
        cars2=int(data['south'])   
        cars3=int(data['east'])
        cars4=int(data['west'])
        temps_vert=brain(cars1,cars2)
    except:
        pass
    print("modification de la maquette")
    AllMightyController.switch_state()
    # AllMightyController.switch_state()#the state changes immediately as frontend asks
    return JsonResponse({"result":temps_vert}, safe=False)


def activate(request):
    #lance la simulation
    global t
    AllMightyController.all_off()
    if t==None or not t.is_alive():
        print("start threading")
        t=threading.Thread(target=AllMightyController.listen, args=(), kwargs={})
        t.setDaemon(True)
        t.start()
    return HttpResponse("started")


def deactivate(request):
    #arrete la simulation
    global t
    AllMightyController.all_off()
    AllMightyController.state_phase1=0
    AllMightyController.state_phase2=0
    if t!=None:
        t.do_run=False
        t.join()
    return HttpResponse("finished")