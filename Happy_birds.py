#!/usr/bin/env python3

import tkinter as tk
import math as m
import matplotlib.pyplot as plt 
#from datetime import datetime, timedelta 
#import time

class App_happy_birds(tk.Tk):
	def __init__(self):
		"""Constructeur de l'application."""
		tk.Tk.__init__(self)
		# gravite
		self.g = 9.8
		self.coef_rappel = 0.5
		self.coef_frottements = 0.0002
		self.widht_fenetre = 1600
		self.height_fenetre = 800
		self.x_center = 200
		self.y_center = self.height_fenetre*2/3
		self.V = 0

		# Diamètre du projectile
		self.diam = 15
		# intervalle de temps entre 2 points
		self.dt = 0.004
		# Création et packing du canvas
		self.canv = tk.Canvas(self, bg='light gray', height=self.height_fenetre,
							  width=self.widht_fenetre, 
							  highlightbackground="black")
		self.canv.pack(side=tk.LEFT)
		# Création du projectile
		self.project = self.canv.create_oval(self.x_center-self.diam/2,
											 self.y_center-self.diam/2,
											 self.x_center+self.diam/2,
											 self.y_center+self.diam/2,
											 fill="black")
		# création des axes
		self.canv.create_line(self.x_center, 0, self.x_center,
							  self.height_fenetre, fill="red", dash=(4, 4))
		self.canv.create_line(0, self.y_center, self.widht_fenetre,
							  self.y_center, fill="red", dash=(4, 4))
		
		self.canv.bind("<Button -1>", self.click)
		self.bind("<space>", self.move)
		self.first = True

		# compteur pour les points de suivis
		self.delay_pnt = 0

		# Initialisation de la vairable représentant 
		# la boucle "after" de la fonction move()
		self.solve = 0
		
		# Create widgets
		self.creat_widgets()

	def creat_widgets(self):
	    self.bouton_restart = tk.Button(self, text=" Restart ",
	    								command=self.restart)
	    self.bouton_restart.pack(side=tk.TOP)
	    self.bouton_quit = tk.Button(self, text=" QUIT ",
	    							 command=self.quitte)
	    self.bouton_quit.pack(side=tk.BOTTOM)

	def click(self, mclick):
		# si l'utilisateur place le projectile après l'absisse du lanceur
		if mclick.x>self.x_center: 
			print("ERROR POSITION")
		else:
			# si un lancé est toujours en cours (boucle move), on l'arrete
			if self.solve != 0: 
				self.after_cancel(self.solve)
			# Si ce n'est pas le premier lancé 
			# effacer l'ancienne trajectoire et l'ancien projectile
			if self.first == False: 
				self.canv.delete(self.project)
				self.canv.delete(self.traj)
			self.first = False

			self.x0 = mclick.x
			self.y0 = mclick.y
			# Initialisation du vecteur (click souris - centre du lanceur)
			nominater = self.y_center-self.y0
			denominateur = self.x_center-self.x0
			self.beta = m.atan(nominater/denominateur)
			self.L = m.sqrt((self.x0-self.x_center)**2 
								+ (self.y0-self.y_center)**2)
			# Création du projectile à la position initiale (click souris)
			self.project = self.canv.create_oval(mclick.x-self.diam,
												 mclick.y-self.diam,
												 mclick.x+self.diam,
												 mclick.y+self.diam,
												 fill="black")
			# Initialisation du vecteur d'indicateur de direction du lancé
			x_final = mclick.x+1.5*self.L*m.cos(self.beta)
			y_final = mclick.y+1.5*self.L*m.sin(self.beta)
			self.traj = self.canv.create_line(mclick.x, mclick.y,
											  x_final, y_final,
											  arrow='last', fill="green",
											  dash=(4, 4))

			# Initialisation des positions, vitesse et temps
			self.x = self.x0
			self.y = self.y0
			self.vitesse_x = 0
			self.vitesse_y = 0
			self.t = 0

	def move(self, event=None):
		# MAJ de l'angle + norme du vecteur (projectile-centre du lanceur)
		self.beta = m.atan((self.y_center-self.y)/(self.x_center-self.x))
		self.L = m.sqrt((self.x-self.x_center)**2 + (self.y-self.y_center)**2)
		
		# Lorsque le prjectile est propulsé par le lanceur
		# la force de rappel du lanceur est non nulle
		if self.x<self.x_center: 
			self.force_rappel = self.coef_rappel*self.L
		else : 
			self.force_rappel = 0

		self.poids = 1/2*self.g
		# Calcule de l'accélé, de la vitesse puis de la position du projectile
		self.acceleration_x = self.force_rappel*m.cos(self.beta) 
		self.acceleration_y = self.force_rappel*m.sin(self.beta) + self.poids

		self.vitesse_x = self.acceleration_x*self.t + self.vitesse_x - \
						 self.coef_frottements*self.vitesse_x**2

		self.vitesse_y = self.acceleration_y*self.t + self.vitesse_y + \
						 self.coef_frottements*self.vitesse_y**2

		self.x = self.vitesse_x*self.t + self.x
		self.y = self.vitesse_y*self.t + self.y
		# MAJ de la position du projectile
		self.canv.coords(self.project, self.x-self.diam, self.y-self.diam,
	 					self.x+self.diam, self.y+self.diam)
		self.t += self.dt # incrémentation du temps


		# mise à jour des points de suivis du projectile
		self.pnt = self.canv.create_oval(self.x, self.y,
		 		self.x+2, self.y+2, fill="blue", width=1)

		# supprime le mouvement du projectile lorsqu'il disparait 
		# verticalement de l'écran
		if (self.y-10*self.diam) > self.height_fenetre:
			self.canv.delete(self.project)
			self.vitesse_x = 0
			self.vitesse_y = 0
			self.t = 0

		self.solve = self.after(15, self.move) # boucle sur la fonction move


	def restart(self):
		self.first = True
		if self.solve != 0 : # Stop la boucle "after" si elle est lancée
			self.after_cancel(self.solve)
		self.canv.delete("all")
		self.vitesse_x = 0
		self.vitesse_y = 0
		self.t = 0

		# création des axes
		self.canv.create_line(self.x_center, 0, self.x_center,
							  self.height_fenetre, fill="red", dash=(4, 4))
		self.canv.create_line(0, self.y_center, self.widht_fenetre,
							 self.y_center, fill="red", dash=(4, 4))
		# Création du projectile
		self.project = self.canv.create_oval(self.x_center-self.diam/2,
											 self.y_center-self.diam/2,
											 self.x_center+self.diam/2,
											 self.y_center+self.diam/2,
											 fill="black")

	def quitte(self):
		self.canv.delete("all")
		self.destroy()

if __name__ == "__main__":
	app = App_happy_birds()
	app.mainloop()

