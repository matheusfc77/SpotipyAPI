import threading

class Pipeline:

    def __init__(self, id):
        self.id = id
        self.lt_objetcs = []


    def add_object(self, order, object, path_read, path_write):
        self.lt_objetcs.append((order, object, path_read, path_write))


    def execute(self):
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
                lt_threads.append(thread)
                thread.start()

            for n in range(len(lt_threads)):
                lt_threads[n].join()

            count_order += 1

