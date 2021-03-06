'''
Created on Jan 30, 2011

@author: snail
'''

from os.path import join
from os import getcwd
import logging, logging.handlers
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
from pickle import dumps
LogPath = "Logs" 

#ensure the logging path exists.
try:
    from os import mkdir
    mkdir(join(getcwd(),LogPath))
    del mkdir
except:
    pass


def CreateLogger(name,level=None):
    l = logging.getLogger(name)
    l.setLevel(DEBUG)
    if level!=None:
        l.setLevel(level)
    
    handler = logging.handlers.RotatingFileHandler(join(LogPath,"%s.log"%name), maxBytes=10240, backupCount=10)
    formatter = logging.Formatter("%(asctime)s|%(thread)d|%(levelno)s|%(module)s:%(funcName)s:%(lineno)d|%(message)s")
    handler.setFormatter(formatter)
    l.addHandler(handler) 
    return l

class LogFile:

    def __init__(self, output, minLevel=WARNING):
        self.minLevel = minLevel
        self._log = CreateLogger(output)
    def debug(self,*vals, **kws):
        self.log(DEBUG,*vals,**kws)
    def note(self,*vals, **kws):
        self.log(INFO,*vals,**kws)
    def info(self,*vals, **kws):
        self.log(INFO,*vals,**kws)
    def warning(self,*vals, **kws):
        self.log(WARNING,*vals,**kws)
    def error(self,*vals, **kws):
        self.log(ERROR,*vals,**kws)
    def critical(self,*vals, **kws):
        self.log(CRITICAL,*vals,**kws)
    def log(self, level, *vals, **kws):
        self._log.log(level,"\t".join(map(str,vals)))


if __name__=="__main__":
    
    import threading, time, random
    class Worker(threading.Thread):
        log = None
        def run(self):
            for i in range(20):
                time.sleep(random.random()*.1)
                if self.log:
                    self.log.warning(i,"abc","123")
    logger = LogFile("test")
    for i in range(20):
        w = Worker()
        w.log = logger
        w.start()
    


