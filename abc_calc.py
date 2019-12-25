import math
import random

class Abc:
  def __init__(self, dim):
    self.dim = dim
    self.employeed_bees_num = 20
    self.onlooker_bees_num = 10
    self.max_trial = 200

  def initialize(self, func):
    self.func = func
    self.sources = [
      func.get_initial_positions(self.dim)
      for _ in range(self.employeed_bees_num)
    ]
    self.fits = [
      self._fit(func(s))
      for s in self.sources
    ]
    self.source_count = [0]*self.employeed_bees_num

  def _fit(self, v):
    try:
        return math.exp(-v)
    except OverflowError:
        return 0
    
  def _compare(self, idx, new_source):
    current_value = self.func(self.sources[idx])
    new_value = self.func(new_source)
    if current_value > new_value:
      self.sources[idx] = new_source
      self.source_count[idx] = 0
      self.fits[idx] = self._fit(new_value)
    else:
      self.source_count[idx] += 1
  
  def _generate_new_source(self, idx, source):
    k = idx
    while k == idx:
      k = random.randint(0, self.employeed_bees_num-1)
    new_source = [
      self.func.adjust_within_range(s + random.uniform(-1, 1) * (s - o))
      for s, o in zip(source, self.sources[k])
    ]
    return new_source

  def _employeed_bees(self):
    new_sources = [0] * self.employeed_bees_num
    for i, source in enumerate(self.sources):
      new_source = self._generate_new_source(i, source)
      new_sources[i] = new_source
  
    for idx in range(self.employeed_bees_num):
      self._compare(idx, new_sources[idx])
  
  def _onlooker_bees(self):
    for _ in range(self.onlooker_bees_num):
      idx = random.choices(range(self.employeed_bees_num), weights = self.fits)[0]
      new_source = self._generate_new_source(idx, self.sources[idx])
      self._compare(idx, new_source)
  
  def _scout_bees(self):
    for i, count in enumerate(self.source_count):
      if count <= self.max_trial:
        continue
      
      self.sources[i] = self.func.get_initial_positions(self.dim)
      self.source_count[i] = 0
      self.fits[i] = self._fit(self.func(self.sources[i]))

  def best_set(self):
    best_source = [0]*self.dim
    best_value = math.inf
    for source in self.sources:
      v = self.func(source)
      if best_value > v:
        best_value = v
        best_source = source

    return best_value, best_source

  def step(self):
    self._employeed_bees()
    self._onlooker_bees()
    self._scout_bees()
