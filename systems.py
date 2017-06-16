import threading
Ship = {}
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
            threading.Thread(target=function,args=(value,)).start()
    def watch(self,name,callback):
        self.watches[name].append(callback)
    def unwatch(self,name,callback):
        self.watches[name].remove(callback)
    def update(self):
        for k, v in self.watches.items():
            for function in v:
                threading.Thread(target=function,args=(self.values[k],)).start()
class Alerts(System):
    def __init__(self):
        System.__init__(self)
        self.add("status",0) #Green Alert
    def changeStatus(self,status): #Intent to change status.
        self.set("status",status)
        return True
class Lights(System):
    def __init__(self):
        System.__init__(self)
        self.add("brightness",0)
    def adjustLights(self,value):
        if Ship["Power"].values["power_lights"] < value:
            return False
        self.set("brightness",value)
        return True
    def power_lights_changed(self,value):
        if value > self.values["brightness"]:
            self.set("brightness",value)
class BatteryPower(System):
    def __init__(self):
        System.__init__(self)
        self.add("available",1000)
class EnginePower(System):
    def __init__(self):
        System.__init__(self)
        self.add("available",0)
class Power(System):
    def __init__(self):
        System.__init__(self)
        self.add("total",0)
        self.add("in_use",0)
        self.add("power_shields",0)
        self.add("power_lights",0)
    def batterypower_changed(self,value):
        self.set("total",value+Ship["EnginePower"].values["available"])
    def enginepower_changed(self,value):
        self.set("total",value+Ship["BatteryPower"].values["available"])
    def totalpower_changed(self,value):
        if self.values["in_use"] > self.values["total"]:
            remaining = self.values["in_use"] - self.values["total"]
            while remaining > 0:
                if self.values["power_lights"] > 0:
                    if self.values["power_lights"] > remaining:
                        self.set("power_lights",self.values["power_lights"]-remaining)
                        remaining = 0
                    else:
                        remaining -= self.values["power_lights"]
                        self.set("power_lights",0)
                if self.values["power_shields"] > 0:
                    if self.values["power_shields"] > remaining:
                        self.set("power_shields",self.values["power_shields"]-remaining)
                        remaining = 0
                    else:
                        remaining -= self.values["power_shields"]
                        self.set("power_shields",0)
            self.set("in_use",self.values["total"])
    def requestPower(self,system,value):
        mag = value - self.values["power_"+system]
        if self.values["in_use"]+mag > self.values["total"]:
            return False
        self.set("in_use",self.values["in_use"]+mag)
        self.set("power_"+system,value)
        return True
class Shields(System):
    def __init__(self):
        System.__init__(self)
        self.add("health",100)
        self.add("status",False)
    def lowerShields(self):
        self.set("status",False)
        return True
    def raiseShields(self): #Intent to raise shields.
        if self.values["status"] == True:
            return True
        if Ship["Power"].values["power_shields"] >= 50 and self.values["health"] >= 50:
            self.set("status",True)
            return True
        return False
    def power_shields_changed(self,value):
        if value < 50:
            self.set("status",False)
    def health_changed(self,value):
        if value < 50:
            self.set("status",False)
def init():
    Ship["Alerts"] = Alerts()
    Ship["Lights"] = Lights()
    Ship["BatteryPower"] = BatteryPower()
    Ship["EnginePower"] = EnginePower()
    Ship["Power"] = Power()
    Ship["Shields"] = Shields()
    Ship["BatteryPower"].watch("available",Ship["Power"].batterypower_changed)
    Ship["Power"].watch("total",Ship["Power"].totalpower_changed)
    Ship["BatteryPower"].update()
init()
print Ship["Power"].requestPower("lights",50)
print Ship["Power"].requestPower("lights",50)
print Ship["Power"].requestPower("lights",50)
print Ship["Power"].requestPower("lights",50)
print Ship["Power"].requestPower("lights",50)
print Ship["Power"].requestPower("lights",50)
print Ship["Power"].requestPower("lights",50)
print Ship["Power"].requestPower("lights",50)
print Ship["Power"].requestPower("lights",50)
print Ship["Power"].requestPower("lights",50)
print Ship["Power"].requestPower("lights",50)

print Ship["Lights"].adjustLights(60)
print Ship["Lights"].adjustLights(60)
print Ship["Lights"].adjustLights(60)
print Ship["Lights"].adjustLights(60)
print Ship["Lights"].adjustLights(60)
print Ship["Lights"].adjustLights(60)
print Ship["Lights"].adjustLights(60)
print Ship["Lights"].adjustLights(60)
print Ship["Lights"].adjustLights(60)
print Ship["Lights"].adjustLights(60)
print Ship["Lights"].adjustLights(60)
print Ship["Lights"].adjustLights(50)
print Ship["Lights"].adjustLights(50)
print Ship["Lights"].adjustLights(50)
print Ship["Lights"].adjustLights(50)
print Ship["Lights"].adjustLights(50)
print Ship["Lights"].adjustLights(50)
print Ship["Lights"].adjustLights(50)
print Ship["Lights"].adjustLights(50)
print Ship["Lights"].adjustLights(50)
print Ship["Lights"].adjustLights(50)
