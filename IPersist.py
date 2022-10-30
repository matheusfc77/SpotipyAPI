
class IPersist:
    '''
    Class for standardizing data persistence
    '''

    def read(self, path): raise NotImplementedError

    def write(self, path, info): raise NotImplementedError