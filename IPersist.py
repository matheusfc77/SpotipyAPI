
class IPersist:

    def read(self, path): raise NotImplementedError

    def write(self, path, info): raise NotImplementedError