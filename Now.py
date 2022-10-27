import datetime
import pytz

class Now:

    def now(self):
        return datetime.datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()