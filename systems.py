import threading
import time
from multiprocessing import Process
class Main:
    def __init__(self):
        self.activities = []
    def start(self):
        for function in self.activities:
            p = Process(target = function, args=())
            p.start()
def watch(name,value):
    def real_decorator(function):
        """try:
            try:
                self.watches[name][value].append(function)
            except AttributeError:
                self.watches[name][value] = []
                self.watches[name][value].append(function)
        except KeyError:
            self.watches[name] = {}
            self.watches[name][value] = []
            self.watches[name][value].append(function)"""
        function.watch = (name,value)
        return function
    return real_decorator
main = Main()
class System:
    def __init__(self):
        self.watches = {}
        main.activities.append(self.run)
    def __setattr__(self,attr,value):
        self.__dict__[attr] = value
        """for function in [a for a in dir(self) if not a.startswith('__')]:
            try:
                if getattr(self,function).watch[0] == attr:
                    value.observe(getattr(self,function).watch[1],getattr(self,function))
            except AttributeError:
                pass"""
        try:
            for function in self.watches[attr]:
                threading.Thread(target=function,args=(value,)).start()
        except KeyError:
            self.watches[attr] = []
    def attach(self,attr,value):
        try:
            self.__dict__[attr].append(value)
        self.__dict__[attr] = value
        for function in [a for a in dir(self) if not a.startswith('__')]:
            try:
                if getattr(self,function).watch[0] == attr:
                    value.observe(getattr(self,function).watch[1],getattr(self,function))
            except AttributeError:
                pass
    def run(self):
        while True:
            try:
                self.newtime = time.time()
                self.delta = self.newtime - self.time
                self.time = self.newtime
            except AttributeError:
                self.delta = 0
                self.time = time.time()
            self.activity()
    def activity(self):
        pass
    def observe(self,value,function):
        try:
            self.watches[value].append(function)
        except KeyError:
            self.watches[value] = []
            self.watches[value].append(function)
class PowerConduit(System):
    def __init__(self,name,priority):
        System.__init__(self)
        self.name = name
        self.power = 0
        self.priority = 0
    def requestPower(self,power):
        mag = power - self.power
        if self.Power.requestPower(mag):
            self.power = power
            return True
        return False
    def changePriority(self,priority):
        self.priority = priority
        return True
    def lowerPower(self,request):
        if request > self.power:
            t = self.power
            self.power = 0
            return t
        else:
            self.power -= request
            return request
class Power(System):
    def __init__(self):
        System.__init__(self)
        self.total = 0
        self.in_use = 0
        self.Source = []
    @watch("Source","available")
    def power_changed(self,value):
        pass
class Lights(System):
    def __init__(self)
        System.__init__(self)
        self.brightness = 0
    def adjustLights(self,value):
        if self.Conduit.power < value:
            return False
        self.brightness = value
        return True
    @watch("Conduit","power")
    def power_changed(self,value):
        if value > self.brightness:
            self.brightness = value
class Alerts(System):
    def __init__(self):
        System.__init__(self)
        self.status = 0
    def changeStatus(self,status):
        self.status = status
        return True
s1 = Alerts()
s2 = Alerts()
s1.attach("Alerts",s2)
#How to handle power?
#main.start()
#Each system stores other systems it needs as attributes.
#Each system has a "start" function that sets up all watches.