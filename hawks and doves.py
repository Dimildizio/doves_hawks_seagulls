'''
Requires Matplotlib library


This script simulates the behaviour of the creatures: 
											1. "doves"  - cowardly (don't fight)
											2. "hawks" - aggressive (always fight to the end)
											3. "seagulls" - semi-aggressive (fight cowards and each other)

with this setup there is a limited amount of food. Each food gets two points.
A creature needs 1 food point to survive to the next day. 
If a creature has less than 1 point it has a (1-points)% chance to die.
If it gets more than 1 point it has a (points-1)) % chance to reproduce.
If two creatures approach same piece of food they compete for it according to the relative weights of their behaviour models.
Every day previous food dissappears, new food spawns, creatures "search" for food, then the kill/reproduce actions are resolved.
To create proper data the amount of days should better be inbetween 1000 and 10000.

Current weights setup:

doves : doves  			   1  :  1  		doves share 
doves : hawks 		 	 0.5  :  1.5 		hawks take 50% of doves' share
doves : seagulls 		 0.75 :  1.25 		seagulls take 25% of doves' share
hawks : hawks 		 	   0  :  0 			hawks waste too much energy and die fighting
hawks : seagulls	 	   1  :  0.75   	seagulls run but lose 25% of their share
seagulls : seagulls 	 0.25  :  0.25 		seagulls fight and lose 75% of their share

Later might want to readjust the weights to energy cost.

Looks like with the current wights setup and amount of food most of the times the doves can't survive through set
number of days. 
'''

from random import random, choice, randint
from matplotlib import pyplot as plt


#weights
chances = {0: {  0:1,
			     1:0.5,
			     2:0.75
			   },
		  1: {  0:1.5,
				1:0,
				2:1
			  },
		  2: {  0:1.25,
				1:0.75,
				2:0.25
			  }
			}


class Food:
	def __init__(self):
		self.competer = []

class Creature:
	def __init__(self, behaviour = 1):
		self.behaviour = behaviour
		self.status = 0


class Simulation:
	def __init__(self, days = 1000):
		self.creatures = []
		self.stock = []

		self.total = {0:[], 1:[], 2:[]}
		self.days = days

		self.populate()
		self.create_data()
		self.plot_sim()

	def create_data(self):
		#collecting data for amount of days
		for d in range(self.days):
			self.day()

	def plot_sim(self):
		#print total amount of creatures and the creature type % in total for all days and for last day
		#plots data to the graph 
		per = lambda x,t: (round(x/t, 2)*100)
		d,h,s = sum(self.total[0]), sum(self.total[1]), sum(self.total[2])
		ld,lh,ls = self.total[0][-1], self.total[1][-1], self.total[2][-1]
		tot, ltot = d+h+s, ld+lh+ls
		text = f'In total:\n\tdoves: {d} ({per(d,tot)}%)\n\t hawks: {h} ({per(h,tot)}%)\n\t seagulls: {s} ({per(s,tot)}%)\n\t\t total: {tot}'
		last_day = f'Last day: \n\tdoves:{ld} ({per(ld,ltot)}%)\n\thawks {lh} ({per(lh,ltot)}%)\n\tseagulls: {ls} ({per(ls,ltot)})%\n\t\ttotal: {ltot}\n\t\tstock: {len(self.stock)}'
		print(text, last_day, sep = '\n')

		plt.stackplot([x for x in range(1,self.days+1)], self.total[0], self.total[1], self.total[2], labels = ['doves', 'hawks', 'seagulls'])
		plt.legend(loc='upper left')
		plt.xlabel('days')
		plt.ylabel('population')
		plt.title('doves, hawks and seagulls')
		plt.suptitle('Simulation')
		plt.show()


	def populate(self):
		#creates 2 creatures of each kind
		self.creatures = [Creature(x) for x in range(3) for duplicates in range(2)]
		

	def restock(self):
		#creates food
		self.stock = [Food() for foo in range(randint(100,150))] #some randomness to the food amount

		
	def summary(self):
		#counts daily amount of creatures
		birds = {0:0,1:0,2:0}
		for creature in self.creatures:
			birds[creature.behaviour] += 1
		for cr in birds:
			self.total[cr].append(birds[cr])
			

	def feed_creatures(self):
		#"hunt" for food. creature finds food and add self to it. if another creature finds it 
		#both creatures' status changes according to the weights of their behaviours  
		for creature in self.creatures:
			if self.stock:
				food = choice(self.stock)
				food.competer.append(creature)
				creature.status = 2
				if len(food.competer) > 1:
					rival = food.competer[0]
					rival.status = chances[rival.behaviour][creature.behaviour]
					creature.status = chances[creature.behaviour][rival.behaviour]
					self.stock.remove(food)

	def day(self):
		self.restock()
		self.feed_creatures()
		self.judgement_time()
		self.summary()

	def judgement_time(self):
		#daily kill\reproduce routine
		for creature in self.creatures:
			r = random()
			if r > creature.status:
				self.kill_creature(creature)
				continue
			elif r+1 < creature.status:
				self.reproduce_creature(creature)

	def kill_creature(self, creature):
		self.creatures.remove(creature)

	def reproduce_creature(self, creature):
		self.creatures.append(Creature(creature.behaviour))



sim = Simulation()
