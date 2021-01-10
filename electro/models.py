from django.db import models

# Create your models here.
class Feux(models.Model):
    green = models.SmallIntegerField(default=0)
    orange = models.SmallIntegerField(default=0)
    red = models.SmallIntegerField(default=0)
    green_duration = models.IntegerField(default=10)
    orange_duration = models.IntegerField(default=7)
    red_duration = models.IntegerField(default=5)

    def setGreen(self):
        self.green = 1
        self.orange = 0
        self.red = 0
        self.save()

    def setOrange(self):
        self.green = 0
        self.orange = 1
        self.red = 0
        self.save()

    def setRed(self):
        self.green = 0
        self.orange = 0
        self.red = 1
        self.save()

    def setDuration(self, greenDuration, orangeDuration, redDuration):
        self.green_duration = greenDuration
        self.orange_duration = orangeDuration
        self.red_duration = redDuration
        self.save()

    def __str__(self):
        if self.green == 1:
            return "Feux Vert"
        elif self.orange == 1:
            return "Feux Orange"
        elif self.red == 1:
            return "Feux Rouge"
        else:
            return "Aucun feux"

class Voie(models.Model):
    NAMES = (
        ('NORTH', 'NORTH'),
        ('SOUTH', 'SOUTH'),
        ('WEST', 'WEST'),
        ('EAST', 'EAST')
    )
    name = models.CharField(choices=NAMES, null=False, max_length=10)
    nombre_voiture = models.IntegerField(default=0)
    feux = models.ForeignKey(Feux, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " " + str(self.nombre_voiture)

    def setVoiture(self, nombre):
        self.nombre_voiture = nombre
        self.save()
    
