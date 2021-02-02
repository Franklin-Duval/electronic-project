import random
from django.shortcuts import redirect, render
from django.http import Http404
from django.http import JsonResponse,HttpResponse
from .brain import brain
from django.views.decorators.csrf import csrf_exempt
import time
import threading
from gpiozero import DistanceSensor # detecteur de distance


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

threadForUpdatingState=None
transitions=[0,1,2,2]#l'etat initial de deux feux est 0 et pour les deux autres c'est 2, le contenu du tableau est les indices des feux alumes

#contient les numero de toutes les leds, numerotees de 1 à 4 dans cet ordre et les feux du vert au rouge CE TABLEAU NE DOIT JAMAIS CHANGER
# exple : LEDS=[(23,4,5),(5,4,1),(6,4,6),(13,3,5)]
# qui veut dire que le feu 1 est constitué des leds aux pins 23,4,5


#######################################################

#           CLASSE UTILITAIRE

#######################################################

class TrafficController():
    def __init__(self,leds,sensors):
        self.nb=nb
        self.leds=leds
        self.state_phase1=0
        self.state_phase2=2
        #enregistrement des voies
        for _,i in enumerate(self.leds):
            self.voie[i]=0

        # enregistrement des senseurs
        for ((a1,a2),(b1,b2)),i in enumerate(sensors)):
            self.sensors[i]=(None,None)
            self.sensors[i][0]=DistanceSensor(a1,a2)#senseur voie
            self.sensors[i][1]=DistanceSensor(b1,b2)#senseur voie

    def all_off(self):
        #eteint tout le monde
        for light in self.leds:
            for led in light:
                GPIO.output(led,GPIO.LOW)

    def all_off(self):
        #allume tout le monde
        for light in self.leds:
            for led in light:
                GPIO.output(led,GPIO.HIGH)

    def set_led_on(self,index_led,index_feu):
        #allume une led precise sur un feu
        assert index_led>=0 and index_led<=3 and index_feu>=0 and index_feu<=2
        for led in self.leds[index_led]:
            GPIO.output(led,GPIO.LOW)
        GPIO.output(self.leds[index_feu],GPIO.HIGH)#ce qu'on veut vraiment alumer

        
    def listen(self):
        #cette fonction permet d'ecouter les capteurs ultrasons et mettre a jour les variables 
        t=threading.currentThread()
        while getattr(t,"do_run",True):
            #ecoute des senseurs de distance et mise a jour des parametres
            for sensor,i in enumerate(self.sensors):
                if(sensor[0].distance<seuil):
                    self.voie[i]+=1
                if(sensor[1].distance<seuil):
                    self.voie[i]-=1
            time.sleep(3)
        print("stopped")

    
    def set_phase1_on(self,led_state):
        #allume une led precise des deux feux d'une phase
        set_led_on(self.leds[0],led_state)
        set_led_on(self.leds[2],led_state)


    def set_phase2_on(self,led_state):
        #allume une led precise des deux feux de l'autre
        set_led_on(self.leds[1],led_state)
        set_led_on(self.leds[3],led_state)



    def switch_state(self):
        #allume les leds en suivant les transitions
        self.state_phase1=(self.state_phase1+1)%4
        self.state_phase2=(self.state_phase2+1)%4
        set_phase1_on(transitions[self.state_phase1])
        set_phase2_on(transitions[self.state_phase2])
        



traffic_controller=TrafficController(leds=[(1,2,3),(3,4,5)],sensors=[((10,11),(4,5)),((7,8),(9,13))])

##############################################################################

#                                  VIEWS

############################################################################


# Create your views here.
def home(request):
    return render("You are at Home!")

@csrf_exempt
def compute_time_send_response(request):
    # compute the time needed and return the green time
    cars1=int(request.POST.get('cars1',0))
    cars2=int(request.POST.get('cars2',0))
    temps_vert=brain(cars1,cars2)
    switch_state()#the state changes immediately as frontend asks
    return JsonResponse({"result":temps_vert}, safe=False)


def activate(request):
    #lance la simulation
    global t
    if t==None or not t.is_alive():
        print("start threading")
        t=threading.Thread(target=background_process, args=(), kwargs={})
        t.setDaemon(True)
        t.start()
    return HttpResponse("main thread content")


def deactivate(request):
    #arrete la simulation
    global t
    global voie1
    t.do_run=False
    t.join()
    return HttpResponse(f"finished, result={voie1}")
    