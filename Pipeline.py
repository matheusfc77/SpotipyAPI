import threading
from Now import Now

class Pipeline(Now):
    '''
    Class for create pipeline of extraction
    '''

    def __init__(self, verbose=True):
        self.lt_objetcs = []
        self.verbose = verbose


    def add_object(self, order, object, path_read, path_write):
        '''
        Method for add object of extraction
        
        Args
            int (order): execution order of object
            ExtractionSpotipy (object): object of extraction
            string (path_read): source data
            string (path_write): local for save the data

        Return
            None
        '''

        self.lt_objetcs.append((order, object, path_read, path_write))


    def execute(self, parallel=True):
        '''
        Method for execution of pipeline

        Args
            boolean (parallel): 
                if True, execute the objects based in the order with threads
                if False, execute the objects in sequential order

        Return
            None
        '''

        if parallel:
            if self.verbose: print("{}: START PARALLEL PIPELINE".format(self.now()))

            count_order = 0
            order_exist = True
            while order_exist:
                lt_object_order = []
                lt_threads = []
                for order, object, path_read, path_write in self.lt_objetcs:
                    if order == count_order:
                        lt_object_order.append((object, path_read, path_write))
                
                if len(lt_object_order) == 0: order_exist = False

                for object, path_read, path_write in lt_object_order:
                    thread = threading.Thread(target=object.extract, args=(path_read, path_write))
                    lt_threads.append((object.__class__, thread))
                    if self.verbose: print("{}: START {} THREAD".format(self.now(), object.__class__))
                    thread.start()

                for object_name, thread in lt_threads:
                    thread.join()
                    if self.verbose: print("{}: END {} THREAD".format(self.now(), object_name))

                count_order += 1
            if self.verbose: print("{}: END PARALLEL PIPELINE".format(self.now()))
            
        else:
            if self.verbose: print("{}: START SEQUENTIAL PIPELINE".format(self.now()))
            for _, object, path_read, path_write in self.lt_objetcs:
                object.extract(path_read, path_write)
            if self.verbose: print("{}: END SEQUENTIAL PIPELINE".format(self.now()))
            

