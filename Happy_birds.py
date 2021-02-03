import tkinter as tk
import math
import matplotlib.pyplot as plt 
from datetime import datetime, timedelta 
import time

class App_happy_birds(tk.Tk):
	def __init__(self):
		"""Constructeur de l'application."""
		tk.Tk.__init__(self)
		# gravite
		self.g = 9.8
		# angle du vecteur vitesse initiale
		self.alpha = 45 # angle en °
		self.coef_rappel = 0.3
		self.widht_fenetre = 1200
		self.height_fenetre = 600
		self.x_center = 200
		self.y_center = self.height_fenetre*2/3
		self.V = 0

		# Diamètre du projectile
		self.diam = 15
		# intervalle de temps entre 2 points
		self.dt = 0.005
		# Création et packing du canvas
		self.canv = tk.Canvas(self, bg='light gray', height=self.height_fenetre, width=self.widht_fenetre, highlightbackground="black")
		self.canv.pack(side=tk.LEFT)
		# Création du projectile
		self.project = self.canv.create_oval(self.x_center-self.diam/2, self.y_center-self.diam/2,
							 self.x_center+self.diam/2, self.y_center+self.diam/2, fill="black")
		# création des axes
		self.canv.create_line(self.x_center, 0, self.x_center, self.height_fenetre, fill="red", dash=(4, 4))
		self.canv.create_line(0, self.y_center, self.widht_fenetre, self.y_center, fill="red", dash=(4, 4))
		
		self.canv.bind("<Button -1>", self.click)
		self.first = True

		# compteur pour les points de suivis
		self.delay_pnt = 0
		
		# Create widgets
		self.creat_widgets()


	def click(self, mclick):
		if mclick.x>self.x_center:
			print("ERROR POSITION")
		else:
			if self.first == False:
				self.canv.delete(self.project)
				self.canv.delete(self.traj)
			self.first = False

			self.x0 = mclick.x
			self.y0 = mclick.y
			self.beta = math.atan((self.y_center-self.y0)/(self.x_center-self.x0))
			self.L = math.sqrt((self.x0-self.x_center)**2 + (self.y0-self.y_center)**2)
			self.project = self.canv.create_oval(mclick.x-self.diam, mclick.y-self.diam,
								 mclick.x+self.diam, mclick.y+self.diam, fill="black")
			self.traj = self.canv.create_line(mclick.x, mclick.y, 
						mclick.x+1.5*self.L*math.cos(self.beta), 
						mclick.y+1.5*self.L*math.sin(self.beta), arrow='last',  fill="green", dash=(4, 4))


			self.x = self.x0
			self.y = self.y0
			self.vitesse_x = 0
			self.vitesse_y = 0
			self.t = 0
			# self.move()

	# def trajectoire_1(self, time):
	# 	self.beta = math.atan((300-self.y)/(300-self.x))
	# 	self.x_appui = 300+(300-self.x0)
	# 	self.y_appui = 300-(self.y0-300)
	# 	self.L = math.sqrt( (self.x-self.x_appui)**2 + (self.y-self.y_appui)**2 )
	# 	x = self.x + self.coef_rappel*self.L*time**2*math.cos(self.beta) + self.V*math.cos(self.beta)*time
	# 	y = self.y + self.coef_rappel*self.L*time**2*math.sin(self.beta) + self.V*math.sin(self.beta)*time
	# 	V = math.sqrt((x-self.x)**2+(y-self.y)**2)/self.dt
	# 	return x, y, V

	# def trajectoire_2(self, time):
	# 	x = self.Vx0*time + self.x0
	# 	y = 1/2*self.g*time**2 - self.Vy0*time + self.y0
		# return x, y

	def creat_widgets(self):
	    self.bouton_start = tk.Button(self, text=" Start ", command=self.move)
	    self.bouton_start.pack(side=tk.TOP)
	    self.bouton_restart = tk.Button(self, text=" Restart ", command=self.restart)
	    self.bouton_restart.pack(side=tk.TOP)
	    self.bouton_quit = tk.Button(self, text=" QUIT ", command=self.quitte)
	    self.bouton_quit.pack(side=tk.BOTTOM)

	def move(self):
		print("GO")
		self.beta = math.atan((self.y_center-self.y)/(self.x_center-self.x))
		self.L = math.sqrt((self.x-self.x_center)**2 + (self.y-self.y_center)**2)

		if self.x<self.x_center:
			self.force_rappel = self.coef_rappel*self.L
		else : 
			self.force_rappel = 0
		self.poids = 1/2*self.g
		self.acceleration_x = self.force_rappel*math.cos(self.beta)
		self.acceleration_y = self.force_rappel*math.sin(self.beta) + self.poids
		self.vitesse_x = self.acceleration_x*self.t + self.vitesse_x
		self.vitesse_y = self.acceleration_y*self.t + self.vitesse_y
		self.x = self.vitesse_x*self.t + self.x
		self.y = self.vitesse_y*self.t + self.y
		self.canv.coords(self.project, self.x-self.diam, self.y-self.diam,
	 					self.x+self.diam, self.y+self.diam)
		print(self.force_rappel, self.poids)
		self.t += self.dt

		#if self.delay_pnt == 5:
			# mise à jour des points de suivis
		self.pnt = self.canv.create_oval(self.x, self.y,
		 		self.x+2, self.y+2, fill="blue", width=1)
			#self.delay_pnt = 0
		#self.delay_pnt+=1
		self.solve = self.after(10, self.move)
	# 	# time1 = datetime.now()
	# 	if self.relais == True :
	# 		# Calcule de la trajectoire du projectile
	# 		if self.x < 300:
	# 			self.x, self.y, self.V0 = self.trajectoire_1(self.t)
	# 		else :
	# 			if self.bollean == True:
	# 				# time2 = datetime.now()
	# 				# print(time2-time1)
	# 				self.x0 = self.x
	# 				self.y0 = self.y
	# 				# Vitesse initiale du projectile
	# 				self.Vx0 = self.V0*math.cos(self.beta)
	# 				self.Vy0 = -self.V0*math.sin(self.beta)
	# 				self.t = 0
	# 				self.bollean = False
	# 			self.x, self.y = self.trajectoire_2(self.t)
			
	# 		# mise à jour des coord boule
	# 		self.canv.coords(self.project, self.x-self.diam, self.y-self.diam,
	# 					self.x+self.diam, self.y+self.diam)
	# 		self.t += self.dt


	# 		self.after(1, self.move)
	# 	self.relais = True

	def restart(self):
		self.first = True
		self.after_cancel(self.solve)
		self.canv.delete("all")
		self.canv.delete(self.project)
		self.canv.delete(self.traj)
		self.vitesse_x = 0
		self.vitesse_y = 0
		self.t = 0

		# création des axes
		self.canv.create_line(self.x_center, 0, self.x_center, self.height_fenetre, fill="red", dash=(4, 4))
		self.canv.create_line(0, self.y_center, self.widht_fenetre, self.y_center, fill="red", dash=(4, 4))

	def quitte(self):
		self.quit()

if __name__ == "__main__":
	app = App_happy_birds()
	app.mainloop()

