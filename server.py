import cherrypy
from cherrypy import expose
from Queue import Queue, Empty

def log(entry):    
    cherrypy.engine.log_cache.put( entry )    
    
class Root:
    
    @expose
    def log(self,*args,**kwargs):
    
        import pickle
        record = pickle.loads( kwargs[ 'record' ] )
        
        log( record )        
        
        return 'Done'    
        
if __name__ == '__main__':        
    
    from logging.handlers import RotatingFileHandler
    handler = RotatingFileHandler('httplogger.txt', maxBytes=2 * 1024, backupCount=5)
    
    def write():
        
        queue = cherrypy.engine.log_cache
            
        while True:
            
            try:                   
                handler.emit( queue.get_nowait() )    
                    
            except Empty, e:
                return       
        
        
    from cherrypy.process import plugins
    
    cherrypy.engine.log_writer = plugins.Monitor(cherrypy.engine,write,15)    
    cherrypy.engine.log_writer.subscribe()
    
    cherrypy.engine.log_cache = Queue()
    app = cherrypy.quickstart( Root(), config = "config.txt" )
    