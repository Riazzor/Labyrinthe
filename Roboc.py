# -*-coding:Utf-8 -*

import sauvegarde.GestionSauvegarde as GS
from DATA import fonction
from mouvement.robot import Robot


print('='*30)
print("BONJOUR".center(30, '='))
print('='*30)
print("LABYRINTHE".center(30, '='))
print('='*30)
print("Quitter : 'ctrl + c'")


end = False
while not end:

	try:

		Robi = Robot()
		gagne = False

		while not gagne:

			fonction.Affichage(lab, obstacles)
			dir, nb = fonction.Deplacement()
			lab, gagne = Robi.mouve(dir, lab, nb)
			GS.sauvegarde(pseudo, lab, obstacles)


		fonction.Affichage(lab, obstacles)
		end = GS.finDePartie(pseudo, lab, obstacles, fin='oui')
		if end == False:
			lab = GS.choixCarte()

	except KeyboardInterrupt:
		end = GS.finDePartie(pseudo, lab, obstacles)
