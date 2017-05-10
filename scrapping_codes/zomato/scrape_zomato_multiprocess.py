import os, psutil, sys, time

from library.city import *
from library.database import *
from multiprocessing import Process
  
from IPython import embed
from time import sleep
from random import randint

GLOBAL_THREADS = 3

def general_scraping(total_threads, thread_number):
  for city in City.select().where(City.finished == False):
    if city.id%total_threads != thread_number :
      continue
    else :
      name = city.name.decode('unicode_escape')
      link = city.link.decode('unicode_escape')
      sys.stdout.write("\nCrawling("+ str(thread_number) +") : " + name.encode('utf-8') + ", " + link.encode('utf-8') + "\n")
      
      if city.pages == 1 :
        city.finished = True
        city.save()

      for page in range(city.pages_crawled + 1, city.pages + 1):
        sys.stdout.write(str(page)+"#"+ str(thread_number))
        y = ScrapeCityBasePage(city, city.link + "?pages" + str(page))


class MyProcessAbstraction(object):
  def __init__(self, parent_pid):
    self._child = None
    self._parent = psutil.Process(pid=parent_pid)

  def run_child(self, total_threads, thread_number):
    print("---- Starting Child: %i of %i ----" % (thread_number, total_threads))
    # self._child = psutil.Popen(self._cmd)
    self._child_pid = os.getpid()
    self.thread_number = thread_number
    self.total_threads = total_threads
    self._child = psutil.Process(pid=self._child_pid)
    sys.stdout.write('---- Parent : '+str(self._parent.pid)+' ## Child : '+str(self._child_pid))
    log_str = '(' + str(thread_number) + ' / ' + str(total_threads) + ') ----'
    try:
      sys.stdout.write("---- Inside Try " + log_str + " ----" + str(self._parent.status()))
      while self._parent.status() == psutil.STATUS_SLEEPING:
        sys.stdout.write("---- Inside While " + log_str)
        sys.stdout = open('/var/log/zomato_scraper_'+str(thread_number)+'_log.txt', 'a+')
        general_scraping(total_threads, thread_number)
        sleep(1)
        break
      sys.stdout.write("---- FINISHED Thread " + log_str)

    except psutil.NoSuchProcess:
      sys.stdout.write("---- Inside Except " + log_str)
      pass

    finally:
      sys.stdout.write("---- Terminating child PID %s (%i / %i)----\n" % (self._child.pid, self.thread_number, self.total_threads))
      sys.exit()
      self._child.terminate()


if __name__ == "__main__":
  parent = os.getpid()
  total_threads = GLOBAL_THREADS
  # main_thread_num = randint(0, total_threads-1)
  for thread_number in range(0,total_threads):
    child = MyProcessAbstraction(parent)
    child_proc = Process(target=child.run_child, args=(total_threads, thread_number))
    child_proc.daemon = True
    child_proc.start()

  # general_scraping(total_threads, 0)
  sleep(3600)
  sys.stdout.write('---- Hourly finish of MAIN PROCESS ----' + "\n")
  error

