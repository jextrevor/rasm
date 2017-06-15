class System:
    def __init__(self):
        self.values = {}
        self.watches = {}
    def add(self,name,value):
        self.values[name] = value
        self.watches[name] = []
    def set(self,name,value):
        self.values[name] = value
        for function in self.watches[name]:
            function(value)
    def watch(self,name,callback):
        self.watches[name].append(callback)
    def unwatch(self,name,callback):
        self.watches[name].remove(callback)
class Alerts(System):
    def __init__(self):
        System.__init__(self)
        self.add("status",0)
a = Alerts()
def watch(value):
    print "Hello this is ",
    print value
a.watch("status",watch)
a.set("status",1)