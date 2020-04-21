import os
import sys
sys.path[:0] = ['../']
from DATA import fonction
from sauvegarde import GestionSauvegarde as GS


""" Ce module va contenir la classe robot qui sera représenté dans le jeu par 'X'.
	X aura des coordonnées pour attributs et des méthodes pour le déplacement."""



class Robot:
	"""La classe du robot à déplacer."""


	def __init__(self):
		"""abs sera l'abscisse(emplacement sur la ligne) et ord l'ordonne(sur la colonne).
			abs et ord sont déterminé avec la lecture de la carte neuve.
			Les déplacements se feront en modifiants directement ces attributs.
			ex : vers le nord : ord -= 1
				 vers l'est : 	abs += 1...
			"""
		_saving = GS.GestionSauvegarde()
		print(_saving.__dict__)

		abs = 0
		ord = 0

		for i in _saving.lab:
			for j in i:
				if j == 'X':
					self.abs = abs
					self.ord = ord
				abs += 1
			ord += 1
			abs = 0

		fonction.Affichage(_saving.lab, _saving.obstacles)


	def mouve(self):
		"""méthode appelé a chaque tour. dir sera une lettre 'n,s,e,o' pour choisir la direction
			et appelé la méthode correspondante. nb sera le nombre de mouvement.
			Il déplace ensuite X à l'intèrieur de la carte donné en argument.
			Renvoie le nouveau labyrinthe et test si la sortie est atteinte."""

		dir, nb = fonction.Deplacement()

		if dir == 'q':
			continuer = _saving.fin_de_partie()

		else:
			direction = {'n' : self._nord, 's' : self._sud, 'e' : self._est, 'o' : self._ouest}
			peut_bouger = True
			i = 0

			while (i in range(nb)) and peut_bouger:
				# print('test : boucle n°', i+1)
				peut_bouger = direction[dir](_saving.lab)
				i += 1

			abs = 0
			ord = 0

			# on parcourt la carte et on efface l'ancienne position de X
			for i in lab:
				for j in i:
					if j == 'X':
						lab[ord] = lab[ord][:abs] + ' ' + lab[ord][abs+1:]
					abs += 1
				ord += 1
				abs = 0

			# on insère le nouvel emplacement de X
			abs = self.abs
			ord = self.ord

			# On regarde si le nouvel emplacement est la sortie
			continuer = self._winner()

			# on redéfinie la carte
			lab[ord] = lab[ord][:abs] + 'X' + lab[ord][abs+1:]

		_saving.Sauvegarde()
		fonction.Affichage(_saving.lab, _saving.obstacles)
		return continuer # on renvoie la carte pour l'affichage.



	def __repr__(self):
		return "abscisse : {}, ordonne : {}".format(self.abs, self.ord)

	def _nord(self, lab):
		"""Déplacement du robot vers le haut de l'écran. Renverra True si le mouvement est possible,
			False sinon."""
		nvll_ord = self.ord - 1
		if nvll_ord >= 0:
			if lab[nvll_ord][self.abs] not in '0':
				# print('test1')
				self.ord = nvll_ord
				peut_bouger = True
			else:
				print("vous ne pouvez pas, c'est un mur!")
				peut_bouger = False

		else:
			peut_bouger = False


		return peut_bouger

	def _sud(self, lab):
		"""Déplacement du robot vers le bas de l'écran. Renverra True si le mouvement est possible,
			False sinon."""
		nvll_ord = self.ord + 1
		if  nvll_ord < len(lab):
			if lab[nvll_ord][self.abs] not in '0':
					self.ord = nvll_ord
					peut_bouger = True
			else:
				print("vous ne pouvez pas, c'est un mur!")
				peut_bouger = False

		else:
			peut_bouger = False

		return peut_bouger

	def _est(self, lab):
		"""Déplacement du robot vers la droite de l'écran. Renverra True si le mouvement est possible,
			False sinon."""

		nvll_abs = self.abs + 1
		if nvll_abs < len(lab[0]):
			if lab[self.ord][nvll_abs] not in '0'  :
				self.abs = nvll_abs
				peut_bouger = True
			else:
				print("vous ne pouvez pas, c'est un mur!")
				peut_bouger = False

		else:
			peut_bouger = False

		return peut_bouger

	def _ouest(self, lab):
		"""Déplacement du robot vers la gauche de l'écran. Renverra True si le mouvement est possible,
			False sinon."""
		nvll_abs = self.abs - 1
		if nvll_abs >= 0 :
			if lab[self.ord][nvll_abs] not in '0':
				self.abs = nvll_abs
				peut_bouger = True

			else:
				print("vous ne pouvez pas, c'est un mur!")
				peut_bouger = False

		else:
			peut_bouger = False

		return peut_bouger

	def _winner(self):
		"""Renvoie True si on a atteint la sortie. Test effectué après chaque nouveau déplacement.
			De cette manière on regarde si le futur emplacement de self est occupé par la sortie."""

		if self.lab[self.ord][self.abs] == 'U':
			print('='*30)
			print('VOUS AVEZ GAGNE!!!')
			print('='*30)


			continuer = _saving.fin_de_partie(fin='oui')

		else:
			continuer = True

		return continuer


if __name__ == "__main__":

	os.system("pause")
