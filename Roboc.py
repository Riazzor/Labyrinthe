# -*-coding:Utf-8 -*
import sauvegarde.GestionSauvegarde as GS
from DATA import Fonction
from mouvement.robot import Robot


print('='*30)
print("BONJOUR".center(30, '='))
print('='*30)
print("LABYRINTHE".center(30, '='))
print('='*30)
print("Quitter : 'ctrl + c'")



roby = Robot()
continuer = True
i = 0
while continuer:

	continuer = roby.mouve()
	i += 1
	#GS._Sauvegarde(pseudo, lab, obstacles)
