import string


def Deplacement():
	"""fait choisir le déplacement ( + le nombre) à chaque tour au joueur.
		Renvoie la direction choisie et le nombre de déplacement."""
	direction = ('n', 's', 'e', 'o', 'q')

	# chx = fonction.ChoixLettre("tentative", *direction)
	chx = ''
	while chx == '':
		chx = input("Dans quel direction?").lower()
		if len(chx) == 1:		# si le joueur n'entre qu'un seul caractère
			if chx not in direction:
				print("choix incomprehensible :", '/'.join(direction), "+ nombre de coup")
				chx = ''
				continue

			else:
				dir = chx
				nb = 1

		elif len(chx) in range(2,4):	# si il entre aussi le nombre de coup
										#jusqu'à 2 chiffre pour le nombre de coup
			try :
				dir = chx[0]
				nb = int(chx[1:])

				if chx[0] not in direction:
					print("choix incomprehensible :", '/'.join(direction), "+ nombre de coup")
					chx = ''
					continue

				elif type(int(chx[1:])) is not int or int(chx[1:]) < 0:
					print("choix incomprehensible :", '/'.join(direction), "+ nombre de coup")
					chx = ''
					continue

			except ValueError:
				print("choix incomprehensible :", '/'.join(direction), "+ nombre de coup")
				chx = ''
				continue

		else:
			chx = ''
			print("choix incomprehensible :", '/'.join(direction), "+ nombre de coup")
			continue

	return dir, nb


def ChoixLettre(*val):#lettre choisi(pour le mot ou pour une question en oui/non)
	"""
	Renvoie le choix de l'utilisateur. soit une lettre de l'alphabet,
	soit l'un des choix proposé(minimum 2). Dans ce cas, le premier argument doit être le
	message adressé au joueur.
	Sinon, écrire le message tout seul."""



	#première boucle à effectuer si choix libre
	if len(val) < 2 or val == ():

		ListeAlpha = list(string.ascii_letters)	#le choix devra etre dans l'alphabet

		if len(val) == 1:
			print(val[0])						#si message à afficher
		chx = ""
		while chx == "":						#boucle tant que choix insatisfaisant
			chx = input("\nEntrez une lettre :")
			if chx not in ListeAlpha:
				print("\nVous devez entrer une lettre!")
				chx = ""

	#deuxième pour que le choix correspondent aux paramètres entrés.
	else:
		chx = ""
		print("\n" + val[0])
		val = list(val)
		del val[0]								#Une fois le message afficher, on peut le supprimer
		while chx == "":
			print("/".join(val))
			chx = input()
			chx = chx.lower()
			print()
			if chx not in val:
				print("\nvous devez choisir", " ou ".join(val))
				chx = ""


	return chx



def Affichage(lab, obstacles):

	"""Fonction qui se contente d'afficher la carte."""

	abs = 0
	ord = 0
	listeObs = list(obstacles.values())



	for i in lab:
		for j in i:
			for obs in listeObs:
				if (abs, ord) == obs[1] and j != 'X':
					j = obs[0]
			print(j, end = '')
			abs += 1


			# if (abs, ord) in obstacles.values() and j != 'X':	# si un emplacement d'obstacle n'est pas occupé par X on l'affiche
				# print('.', end = '')
			# else :
				# print(j, end = '')
			# abs += 1

		ord += 1
		abs = 0
		print()
