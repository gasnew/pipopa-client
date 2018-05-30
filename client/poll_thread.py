from threading import Thread
from utils import record

class PollThread(Thread):
  def __init__(self, poll):
    Thread.__init__(self)
    self.poll = poll

  def run(self):
    self.poll()
