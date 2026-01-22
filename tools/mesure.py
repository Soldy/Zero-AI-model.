import sys
import math
import time
from multiprocessing import Queue, Process

def mesure(
  queue_ :Queue,
  name_:str,
  func_:callable,
  var_:any)->None:
    start = time.time()
    out=func_(var_)
    end = time.time()
    time_spent = math.ceil(end*1000) - math.floor(start*1000)
    queue_.put({
      'out':out,
      'time' : time_spent
    })


class Timer:
    def __init__(self,):
        self._timers={}
    def mesureTimeout(
      self,
      name_:str,
      func_:callable,
      var_:any,
      timeout :int)->any:
        out = []
        looped = 0
        timeout = (timeout*100)
        queue = Queue()
        proc = Process(
          target=mesure,
          args=(queue,
          name_,
          func_,var_,))
        self._timers[name_] = 'timed out'
        proc.start()
        while True:
            time.sleep(0.01)
            looped = looped + 1
            if queue.empty() == False:
                packet = queue.get()
                self._timers[name_] = packet['time']
                out = packet['out']
                proc.join()
                break
            if looped > timeout:
                proc.terminate()
                time.sleep(0.1)
                break
        return out
    def mesure(
      self,
      name_:str,
      func_:callable,
      var_:any)->any:
        sys.stdout.write(name_ + ' : ')
        sys.stdout.flush()
        out = self.mesureTimeout(
          name_,
          func_,
          var_,
          180
        )
        print(str(self._timers[name_]))
        print('count : '+str(len(out)))
        return out
    def mesureCount(
      self,
      name_:str,
      func_:callable,
      var_:any)->any:
        out = self.mesure(
          name_,
          func_,
          var_
        )
        return out
    def print(self)->None:
        print(self._timers)

