import os
import pickle
import sys
sys.path[:0]=['../']
from DATA import fonction
# from mouvement.robot import robot

"""Gestion des différentes sauvegardes de parties. Les fichiers de sauvegarde se termineront
	en '.lab' et seront tous dans le même dossier sauvegarde avec une hiérarchie selon le type de sauvegarde.
	"""
class GestionSauvegarde():
	"""Classe a créer pour la gestion des sauvegardes.
	Classe a appelé dans la classe robot"""


	def __init__(self):
		"""En se créant il demandera le pseudo, la carte.
		la liste d'obstacles est alors créer."""
		self.pseudo, self.lab, self.obstacles = self._choix_pseudo()

	def _choix_pseudo(self):	#va servir à lister les pseudos des joueurs. Permettra ensuite de lancer les parties.
		"""on fait choisir au joueur son pseudo. Ce pseudo est ajouter a la liste des pseudos.
			Si elle n'existe pas on l'a crée.
			Choix de carte si nouvelle partie, chargement de la partie si elle existe.
			Renvoie le pseudo, le labyrinthe et la liste d'obstacle qui seront
			défini comme attributs de l'instance."""

		pas_de_pseudo = True
		while pas_de_pseudo:													#on s'assure d'avoir un pseudo de choisi.
			pseudo = ''
			while pseudo == '':
				pseudo = input("Choisissez le pseudo : \n")
				if pseudo == '' or len(pseudo) < 3:
					print("minimum 3 caractères alpha-numérique")
					pseudo = ''


			chemin = os.getcwd()
			chemin += '/sauvegarde/Pseudo'
			fichier_pseudo = chemin + '/pseudo.lab'

			try:																#si une liste de pseudo existe, on la récupère.
				with open(fichier_pseudo, 'rb') as fichier:
					mon_pickle = pickle.Unpickler(fichier)
					liste_pseudo = mon_pickle.load()

				if pseudo in liste_pseudo:											#si le pseudo existe, on récupère la partie.

					lab, obstacles = self._chargement(pseudo)
				else:																#sinon on demande au joueur s'il veut une nouvelle partie
					print(liste_pseudo)
					chx = fonction.Affichage("Ce pseudo n'existe pas, voulez-vous lancer une nouvelle partie?", 'o', 'n')
					if chx == 'o':
						liste_pseudo.append(pseudo)
						lab, obstacles = self._nouvelle_partie(pseudo)
					else:															#s'il ne veut pas, on relance la saisie du pseudo
						continue

			except FileNotFoundError: 											# autrement, on crée une nouvelle liste de pseudo. Cela implique une nouvelle partie.
				liste_pseudo = []
				liste_pseudo.append(pseudo)
				lab, obstacles = self._nouvelle_partie(pseudo)

			pas_de_pseudo = False


		with open(fichier_pseudo, 'wb') as fichier:								#on sauvegarde la liste de pseudo
			mon_pickle = pickle.Pickler(fichier)
			mon_pickle.dump(liste_pseudo)

		return pseudo, lab, obstacles


	def choixCarte(self):
		#choix de la carte
		"""Liste les cartes possibles. Fait ensuite choisir le joueur.
			la carte est renvoyer sous forme de liste."""

		# On récupère le chemin des cartes
		chemin = os.getcwd()
		chemin += '/sauvegarde/Cartes'
		liste_fichier = os.listdir(chemin)

		liste_carte = []

		for mappe in liste_fichier:
			i = mappe.find('.')
			liste_carte.append(mappe[:i])

		# on affiche les cartes et on fait choisir une carte
		carte = ''
		while carte == '':
			for mappe in liste_carte:
				print(mappe)
			carte = input("Choisissez une carte : \n")

			if carte not in liste_carte:
				print("erreur! vérifiez l'orthographe.")
				carte = ''

		# pour le chargement
		carte = '/' + carte + '.txt'
		chemin += carte

			# on transforme la carte en liste pour l'affichage
		with open(chemin, 'r') as fichier:
			ma_carte = fichier.read()
			lab = ma_carte.split('\n')

		return lab


	def fin_de_partie(self, pseudo, lab, obstacles, fin = 'non'):
		"""fonction appelée si carte terminée ou si le joueur désire quitter la partie.
			La partie est supprimée si le jeu est terminé."""

		choix = fonction.ChoixLettre("Voulez-vous quittez la partie?", 'o', 'n')
		if fin == 'non':
			self.sauvegarde(pseudo, lab, obstacles)
		# si la carte est terminé, on supprime la sauvegarde pour le choix d'un nouvelle carte.
		else:
			self._suppression(pseudo)


		if choix == 'o':

			return True

		else:
			return False




	#sauvegarde de la partie sans qu'elle soit terminée.
	def sauvegarde(self, pseudo, lab, obstacles):	#lab sera la liste contenant le labyrinthe et pseudo sera le pseudo du joueur.
											# Il va falloir rajouter dans la sauvegarde la liste des obstacles pour l'affichage après re-jeux.
		"""fonction de sauvegarde appelé à chaque déplacement et à la fermeture du jeu.
			on inclus le pseudo pour le nom de la sauvegarde, et lab et obstacles qui seront contenus dans le fichier de sauvegarde."""
		pseudo = '/' + pseudo + '.lab'
		chemin = os.getcwd()
		chemin += '/sauvegarde/Partie'
		chemin += pseudo

		fichier_sauvegarde = {'carte' : lab, 'obstacles' : obstacles}

		with open(chemin, 'bw') as sauve:
			mon_pickle = pickle.Pickler(sauve)
			mon_pickle.dump(fichier_sauvegarde)



	def _nouvelle_partie(self, pseudo):
		"""fonction qui récupère la carte.
		On sauvegarde ensuite la partie."""

		lab = self.choixCarte()

		# On va créer un dictionnaire des obstacles du labyrinthe. Pour l'instant de simple porte.
		obstacles = {}
		abs, ord = 0, 0
		x = 0

		for i in lab:
			for j in i:
				if j not in '0 X':
					cle = 'obstacle n°' + str(x)
					obstacles[cle] = [j, (abs, ord)]
					x += 1
				abs += 1
			ord += 1
			abs = 0
		# for i in lab:
			# print(i)
		self.sauvegarde(pseudo, lab, obstacles)

		return lab, obstacles



	#chargement d'une partie entamée non terminée
	def _chargement(self, pseudo):
		""" Va chercher la partie correspondant au pseudo.
			On considère le pseudo déjà verifié."""

		chemin = os.getcwd()
		chemin += '/sauvegarde/Partie'

		pseudo = '/' + pseudo + '.lab'

		chemin += pseudo

		with open(chemin, 'br') as charge:
			mon_pickle = pickle.Unpickler(charge)
			fichier_sauvegarde = mon_pickle.load()

		# On récupère la carte d'un coté et les obstacles de l'autre.
		lab = fichier_sauvegarde['carte']
		obstacles = fichier_sauvegarde['obstacles']

		#test de la carte ajouté suite à un bug lors de la fermeture de la partie sans sauvegarde si X est sur la sortie.
		sortie = False
		for i in lab:
			for j in i:
				if j == 'U':
					sortie = True


		if not sortie:
			print("Erreur lors du chargement de la carte : la sortie n'existe pas. \nLa partie va être supprimée")
			_suppression(pseudo)



		return lab, obstacles




	def _suppression(self, pseudo):
		"""Cette fonction est appelé pour supprimer une partie une fois celle-ci gagnée. Egalement si besoin particulier.
			De cette manière, lors de la prochaine connection une nouvelle carte peut-être chargée"""

		pseudo = '/' + pseudo + '.lab'
		chemin = os.getcwd()
		chemin += '/sauvegarde/Partie'
		chemin += pseudo
		os.remove(chemin)






if __name__ == "__main__":


	test = GestionSauvegarde()
	print(test.__dict__)

	os.system("pause")
