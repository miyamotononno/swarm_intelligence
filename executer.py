import sys
import time
import matplotlib.pyplot as plt

import abc_calc
import pso_calc
import functions



class Executer:
  def  __init__(self):
    self.dim = 5
    self.step_num = 3000
    self.sp = functions.Spare()
    self.ra = functions.Rastrigin()
    self.ro = functions.Rosenbrock()
    self.gr = functions.Griewank()
    self.al = functions.Alphin()
    self.tw = functions.TwoNminima()
    self.Pso = pso_calc.Pso(self.dim)
    self.Abc = abc_calc.Abc(self.dim)

  def __call__(self, calc_name):
    func_list = [self.sp, self.ra, self.ro, self.gr, self.al, self.tw]
    e = None
    if calc_name == 'abc':
      e = self.Abc
    elif calc_name == 'pso':
      e = self.Pso
    else:
      print('set abc or pso!')
      return

    for func in func_list:
      logs = []
      start = time.time()
      e.initialize(func)
      for i in range(self.step_num):
        e.step()
        if (i+1)%100 == 0:
          value, _ = e.best_set()
          logs.append([i, value])

      end = time.time()
      value, position = e.best_set()
      print(func.name)
      print("time {0} sec".format(end - start))
      print('value: ', value)
      print('position: ', position)
      self._save_image(logs, calc_name, func.name, value)
      print('----------------------------')

  def _save_image(self, logs, calc_name, func_name, value):
    idx, values = list(zip(*logs))
    plt.plot(idx, values)
    plt.xlabel('steps')
    if value > 0:
      plt.yscale('log')
    plt.grid(which='both')
    plt.suptitle(calc_name + ' + ' + func_name)
    plt.savefig('images/' + calc_name + '_' + func_name + '.png')
    plt.clf()

# main関数
if __name__ == '__main__':
    args = sys.argv
    e = Executer()
    e(args[1])
