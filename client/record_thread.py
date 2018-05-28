from threading import Thread
from utils import record

class RecordThread(Thread):
  def __init__(self, check_abort):
    Thread.__init__(self)
    self.check_abort = check_abort

  def run(self):
    record(self.check_abort)
