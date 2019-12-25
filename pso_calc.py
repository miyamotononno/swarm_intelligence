import math
import random

class Pso:
  def __init__(self, dim):
    self.dim = dim
    self.sample_num = 100
    self.w = 0.01
    self.c1 = 0.01
    self.c2 = 0.02

  def initialize(self, func):
    self.global_position = [0]*self.dim
    self.global_value = math.inf
    self.swarm = [self.Individual(
      self.dim,
      self.w,
      self.c1,
      self.c2,
      func) for _ in range(self.sample_num)]
    
  def step(self):
    for individual in self.swarm:
      individual_value = individual.step(self.global_position)
      if individual_value < self.global_value:
        self.global_value = individual_value
        self.global_position = individual.position

  def best_set(self):
    return self.global_value, self.global_position

  class Individual:
    
    def __init__(self, dim, w, c1, c2, func):
      self.dim = dim
      self.w = w
      self.c1 = c1
      self.c2 = c2
      self.func = func
      self.position = func.get_initial_positions(dim)
      self.velocity = func.get_initial_velocity(dim)

      self.own_best_position = self.position
      self.best_value = math.inf

    def calc_velocity(self, Xg, Xi, X, V):
      r1 = random.random()
      r2 = random.random()
      self.velocity = [self.w*v + self.c1*r1*(xi - x) + self.c2*r2*(xg - x)
        for xg, xi, x, v in zip(Xg, Xi, X, V)]

    def calc_position(self, V, X):
      self.position = [self.func.adjust_within_range(v+x) for v, x in zip(V, X)]

    def step(self, Xg):
      self.calc_velocity(Xg, self.own_best_position, self.position, self.velocity)
      self.calc_position(self.velocity, self.position)
      current_value = self.func(self.position)
      if current_value < self.best_value:
        self.own_best_position =self.position
        self.best_value = current_value

      return current_value
