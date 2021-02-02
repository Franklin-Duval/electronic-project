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


GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)

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
        self.sensors={}
        for i,((a1,a2),(b1,b2)) in enumerate(sensors):
            self.sensors[i]=[None,None]
            self.sensors[i][0]=DistanceSensor(a1,a2)#senseur voie
            #self.sensors[i][1]=DistanceSensor(b1,b2)#senseur voie
            print(f"(({a1},{a2}),({b1},{b2}))" )
            pass

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
        
    def listen(self):
        dist_voie1=0.2
        dist_voie2=0.5
        #cette fonction permet d'ecouter les capteurs ultrasons et mettre a jour les variables 
        t=threading.currentThread()
        while getattr(t,"do_run",True):
            #ecoute des senseurs de distance et mise a jour des parametres
            for sensor,i in enumerate(self.sensors):
                if(sensor[0].distance>0.1):
                    self.voie[i][0]+=1
                    print(f" distance mesuree par le capteur {i} = {sensor[0].distance}",file=sys.stderr)
                # if(sensor[0].distance>=dist_voie1 and sensor[0].distance<=dist_voie2):
                #     self.voie[i][1]+=1
                # if(sensor[1].distance<dist_voie1):
                # #     self.voie[i][0]-=1
                # if(sensor[1].distance>dist_voie1 and sensor[0].distance<=dist_voie2):
                #     self.voie[i][1]-=1
            time.sleep(0.5)
        print("stopped")

    
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

AllMightyController=TrafficController(leds=[(7,5,3),(15,13,11)],sensors=[((24,23),(None,None))])
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
    cars1=int(request.POST.get('cars1',0))
    cars2=int(request.POST.get('cars2',0))
    temps_vert=brain(cars1,cars2)
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
    if t!=None:
        t.do_run=False
        t.join()
    return HttpResponse("finished")