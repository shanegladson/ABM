from mesa import Model, Agent
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner
import random
import numpy as np
from scipy.stats import levy

class WalkerAgent(Agent):
    def __init__(self, unique_id, model, step_length=1):
        super().__init__(unique_id, model)
        self.step_length = step_length
        self.previous_angle = 0
        self.fov = model.fov
    
    def step(self):
        self.move()
        #print(self.previous_angle)
    
    def move(self):
        # Standard levy distribution for step length
        self.step_length = levy.rvs()
        #print(self.step_length)
        angle = self.previous_angle + random.uniform(-self.fov/2, self.fov/2)
        new_position = (self.pos[0]+self.step_length*np.cos(angle), self.pos[1]+self.step_length*np.sin(angle))
        self.model.grid.move_agent(self, new_position)

        self.previous_angle = angle
        
class WorldModel(Model):
    def __init__(self, N, width, height, fov):
        self.num_agents = N
        self.fov = fov
        self.schedule = RandomActivation(self)
        self.grid = ContinuousSpace(width, height, True)
        self.data_collector = DataCollector(agent_reporters={"Position" : "pos"})
        self.running = True
        
        for i in range(N):
            a = WalkerAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (width//2, height//2))
            
    def step(self):
        self.data_collector.collect(self)
        self.schedule.step()