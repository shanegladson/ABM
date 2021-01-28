from mesa import Model, Agent
from mesa.space import ContinuousSpace
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
import random
import numpy as np


class TreeAgent(Agent):
    def __init__(self, unique_id, model, state):
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.state = state # 0:Fresh, 1:On Fire, 2:Burned
    
    def step(self):
        if self.state == 1:
            neighbors = self.model.grid.get_neighbors(self.pos, 3)
            for n in neighbors:
                if n.state == 0:
                    n.state = 1
            self.state = 2
            
class ForestModel(Model):
    def __init__(self, N, width, height):
        self.grid = ContinuousSpace(width, height, True)
        self.scheduler = BaseScheduler(self)
        self.datacollector = DataCollector(model_reporters={
            "Fine" : "numfine",
            "On Fire" : "numfire",
            "Burned" : "numburned"
        })
        self.num_agents = N
        self.numfine, self.numfire, self.numburned = 0, 0, 0
        
        for i in range(self.num_agents):
            a = TreeAgent(i, self, 0)
            self.scheduler.add(a)
            self.grid.place_agent(a, (random.uniform(0,width), random.uniform(0,height)))
        a = TreeAgent(self.num_agents, self, 1)
        self.scheduler.add(a)
        self.grid.place_agent(a, (random.uniform(0,width), random.uniform(0,height)))
            
    def step(self):
        self.count_type()
        self.datacollector.collect(self)
        self.scheduler.step()
        
    def count_type(self):
        fine, onfire, burned = 0, 0, 0
        for a in self.scheduler.agents:
            if a.state == 0:
                fine += 1
            elif a.state == 1:
                onfire += 1
            else:
                burned += 1
        self.numfine = fine
        self.numfire = onfire
        self.numburned = burned