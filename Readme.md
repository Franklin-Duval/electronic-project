# PROJET ELECTRONIQUE : SYSTEME DE COMMANDE ET DE CONTROLE DES FEUX DE SIGNALISATION SUR UN CARREFOUR À 04 VOIES

ce projet est fait dans le cadre du cours *Electronique et interfaçage* dispensé par le Dr. Anne Marie CHANA assisté de M. TABUE  à l'[Ecole Nationale Superieure polytechnique de Yaoundé](www.polytechnique.cm). L’objet est de gérer le fonctionnement des feux de signalisation sur un carrefour à 04 voies au travers d’une application mobile ou web. Il sera
 ainsi possible de contrôler automatiquement et visualiser l’état desdits feux de signalisation. Nous pourrons ainsi mettre en pratique un certains nombres de notions apprises notamment l’utilisation des capteurs et du mini ordinateur Rasbery PI. ce repository represente le backend du projet permettant de controler les GPIO du raspberry Pi, à associer au frontend fourni avec le projet pour être pleinement fonctionnel.

## Comment deployer l'application
Recuperer le code source sur un Raspberry Pi via la commande: 
- `git pull origin https://github.com/Franklin-Duval/electronic-project/ `

Lancer le serveur Django pour être disponible en externe : 
- `cd electronic-project`
- `py manage.py runserver 0.0.0.0:8000`

Connecter le Raspberry sur un reseau où la machine contenant le frontend est présent et recuperer l'adresse est obtenue grâce à : 
- `ifconfig`

Le serveur est desormais disponible lorsque le Raspberry Pi est en reseau sur l'adresse de celui-ci sur ledit reseau:

- `http://< IP SUR LE RESEAU>:8000/`

## En cas de probleme contacter

- franklinfrost14@gmail.com
- nnanejunior@gmail.com ([Nprime496](www.github.com/nprime496)) 
