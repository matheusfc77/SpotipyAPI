import datetime
import pytz

class Now:
    '''
    Class for return the local datetime
    '''

    def now(self):
        return datetime.datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()