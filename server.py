import cherrypy
from cherrypy import expose
from Queue import Queue, Empty

class Root:
    
    @expose
    def log(self,*args,**kwargs):
    
        import pickle
        record = pickle.loads( kwargs[ 'record' ] )
        
        cherrypy.engine.log_cache.put( record )        
        
        return 'Done'    
        
if __name__ == '__main__':        
    
    from logging.handlers import RotatingFileHandler
    from logging import Formatter
    
    handler = RotatingFileHandler('httplogger.txt', maxBytes=100 * 1024, backupCount=10)    
    handler.formatter = Formatter("%(asctime)s\t[%(process)s:%(thread)s]\t%(name)s\t%(levelname)s\t%(message)s")
    
    def write():
        
        while True:
            
            try:                 
            
                handler.emit( cherrypy.engine.log_cache.get_nowait() )    
                    
            except Empty:
                return       
        
        
    from cherrypy.process import plugins
    
    cherrypy.engine.log_writer = plugins.Monitor(cherrypy.engine,write,15)    
    cherrypy.engine.log_writer.subscribe()
    
    cherrypy.engine.log_cache = Queue()
    app = cherrypy.quickstart( Root(), config = "config.txt" )
    