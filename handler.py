import logging.handlers

class PickleHttpHandler( logging.handlers.HTTPHandler ):

    def mapLogRecord(self, record):
    
        import pickle        
        res = pickle.dumps( record )
        
        return { 'record' : res }