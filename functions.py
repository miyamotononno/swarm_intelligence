import math
import random
from functools import reduce

class Function:
  mx = 0.0
  mi = 0.0
  def get_initial_positions(self, dim):
    return [random.uniform(self.mi, self.mx) for _ in range(dim)]

  def get_initial_velocity(self, dim):
    return [0]*dim

  def adjust_within_range(self, val):
    if val < self.mi:
      return self.mi
    elif val > self.mx:
      return  self.mx
    else:
      return val


class Spare(Function):
  mx = 5.0
  mi = -5.0
  name = 'Spare Function'
  def __call__(self, X):
    return sum([x**2 for x in X])

class Rastrigin(Function):
  mx = 5.0
  mi = -5.0
  name = 'Rastrigin Function'
  def __call__(self, X):
    return 10*len(X) + sum([x**2 - 10*math.cos(2*math.pi*x) for x in X])

class Rosenbrock(Function):
  mx = 10.0
  mi = -5.0
  name = 'Rosenbrock Function'
  def __call__(self, X):
    ret = 0 
    for i in range(len(X)-1):
      a = 100 * (X[i+1]-X[i]**2)**2
      b =  (1 - X[i])**2
      ret += (a+b)

    return ret

class Griewank(Function):
  mx =  600.0
  mi =  -600.0
  name = 'Griewank Function'
  def __call__(self, X):
    a = 1/4000 * sum([x**2 for x in X])
    b = reduce(lambda x,y: x*y, [math.cos(x/(math.sqrt(idx+1.0))) for idx, x in enumerate(X)])
    return a+b

class Alphin(Function):
  mx = 10.0
  mi = -10.0
  name = 'Alphin Function'
  def __call__(self, X):
    return sum([abs(x * math.sin(x) + 0.1 * x) for x in X])

class TwoNminima(Function):
  mx = 5.0
  mi = -5.0
  name = '2^n minimim Function'
  def __call__(self, X):
    return sum([x**4 - 16 * x**2  + 5 * x for x in X])

