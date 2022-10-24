import ast

from IPersist import IPersist
from Now import Now


class TXTPersist(IPersist, Now):

    def __init__(self, verbose=True):
        self.verbose = verbose


    def read(self, path):
        if self.verbose: print('{}: START READ TXT {}'.format(self.now(), path))

        txt_info = []
        with open(path, 'r') as fp:
            for line in fp:
                x = line[:-1]
                txt_info.append(x)

        lt_id_info = [ast.literal_eval(info)['id'] for info in txt_info]
            
        if self.verbose: print('{}: END READ TXT {}'.format(self.now(), path))
        return lt_id_info


    def write(self, path, info):
        if self.verbose: print('{}: START WRITE TXT {}'.format(self.now(), path))
        with open(path, 'w') as fp:
            for item in info:
                fp.write("%s\n" % item)
        if self.verbose: print('{}: END WRITE TXT {}'.format(self.now(), path))
        