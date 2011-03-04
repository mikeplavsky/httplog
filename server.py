import cherrypy
from cherrypy import expose

def log(entry):
    
    name = entry['name']
    cache = cherrypy.engine.log_cache
    
    if not cache.get(name): 
        cache[name] = []
        
    cache[name].append( entry )    
    
class Root:
    
    @expose
    def log(self,*args,**kwargs):
    
        log( kwargs )        
        return 'Done'    
        
if __name__ == '__main__':        
    
    import logging
    from logging.handlers import RotatingFileHandler
        
    logger = logging.getLogger('MyLogger')
    logger.setLevel(logging.INFO)

    logger.addHandler( RotatingFileHandler('httplogger.txt', maxBytes=2 * 1024, backupCount=5) )
    
    def write():
        
        if cherrypy.engine.log_cache:         
            logger.info( str( cherrypy.engine.log_cache ) )        
            
        cherrypy.engine.log_cache = {}
        
    from cherrypy.process import plugins
    
    cherrypy.engine.log_writer = plugins.Monitor(cherrypy.engine,write,2)    
    cherrypy.engine.log_writer.subscribe()
    
    cherrypy.engine.log_cache = {}
    app = cherrypy.quickstart( Root(), config = "config.txt" )
    