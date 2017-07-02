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
def attach(system1,system2):
    system1.attach(type(system2).__name__,system2)
    system2.attach(type(system1).__name__,system1)
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
        notify(attr)
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
    def notify(self,attr):
        try:
            for function in self.watches[attr]:
                threading.Thread(target=function,args=()).start()
        except KeyError:
            self.watches[attr] = []
#Resilient alert system.
class Alerts(System):
    def __init__(self):
        System.__init__(self)
        self.status = 0
    def changeStatus(self,status):
        self.status = status
        return True
#LED ship-wide lighting system.
class Lights(System):
    def __init__(self):
        System.__init__(self)
        self.brightness = 0
    def changeBrightness(self,brightness):
        if brightness > self.Power.lights:
            return "Insufficient power."
        self.brightness = brightness
        return True
    @watch("Power","lights")
    def power_changed(self):
        if brightness > self.Power.lights:
            self.brightness = self.Power.lights
#4 things need to happen:
#The actual coordinates need to be set. Doesn't require sensors.
#The target rotation needs to be calculated. Requires sensors to determine current position.
#The target rotation needs to be reached. Requires sensors to determine current direction.
#Sensor-based positioning and navigating system.
class Course(System):
    def __init__(self):
        System.__init__(self)
        self.x = 0
        self.y = 0
        self.z = 0
        self.status = False
    def setCourse(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        #Check sensors.
        #Now, calculate the target direction.
        #First, subtract current position (obtained through sensors) from target position.
        #Next, calculate the magnitude using Pythagorean theorem.
        #Next, divide all components by magnitude.
        #Next, calculate pitch by taking the inverse sine of Z.
        #Next, divide X by the cosine of pitch, then take the inverse cosine to find the yaw.
        #Also need to code in exceptions.
        #Set the thrusters to go in that direction.
        return True
    def reorient(self):
        #Check sensors.
        #Now, calculate the target direction.
        #First, subtract current position (obtained through sensors) from target position.
        #Next, calculate the magnitude using Pythagorean theorem.
        #Next, divide all components by magnitude.
        #Next, calculate pitch by taking the inverse sine of Z.
        #Next, divide X by the cosine of pitch, then take the inverse cosine to find the yaw.
        #Also need to code in exceptions.
        #Set the thrusters to go in that direction.
        return True
    def changeStatus(self,status):
        if status == True and self.Repair.course > some config value:
            self.status = True
            return True
        if status == True:
            return "System damaged."
        if status == False:
            self.status = False
            return True
    @watch("Repair","course")
    def damage_changed(self):
        if self.Repair.course < some config value:
            self.status = False
#Power transformer, manager and switcher.
class Power(System):
    def __init__(self):
        System.__init__(self)
#Large lithium-ion power banks.
class Battery(System):
    def __init__(self):
        System.__init__(self)
#Nuclear fusion-based generator.
class Generator(System):
    def __init__(self):
        System.__init__(self)
#Bot-based basic repairing and replacing system.
class Repair(System):
    def __init__(self):
        System.__init__(self)
        self.course = 100
        self.generator = 100
        self.battery = 100
        self.power = 100
        self.sensors = 100
        self.radar = 100
        self.radio = 100
        self.targeting = 100
        self.lasers = 100
        self.security = 100
        self.transporter = 100
        self.thrusters = 100
        self.engine = 100
#Positioning using long-range satellite transmissions, and data analysis.
class Sensors(System):
    def __init__(self):
        System.__init__(self)
#Infrared based positioning and locating system.
class Radar(System):
    def __init__(self):
        System.__init__(self)
#Basic message transciever.
class Radio(System):
    def __init__(self):
        System.__init__(self)
#Semi-accurate positioning and aiming system for use with lasers.
class Targeting(System):
    def __init__(self):
        System.__init__(self)
#Short, high energy laser based weaponry system, powered through capacitor bays.
class Lasers(System):
    def __init__(self):
        System.__init__(self)
#Intercom system for security teams.
class Security(System):
    def __init__(self):
        System.__init__(self)
#Shuttle-based transporter system
class Transporter(System):
    def __init__(self):
        System.__init__(self)
#Using sensors, a high precision orienting system.
class Thrusters(System):
    def __init__(self):
        System.__init__(self)
#Switchable highly reflective ship armour.
class Armor(System):
    def __init__(self):
        System.__init__(self)
#The target velocity needs to be calculated. This involves calculating the ship's current pitch and yaw and making a directional vector, then multiplying it by the target speed.
#Next, the difference between the target velocity and the current velocity needs to be calculated.
#Next, the engine needs to normalize the difference, and apply a force along it.
#Multi-direcitonal ion thruster propulsion system.
class Engine(System):
    def __init__(self):
        System.__init__(self)
s1 = Alerts()
s2 = Alerts()
s1.attach("Alerts",s2)
#How to handle power?
#main.start()
#Each system stores other systems it needs as attributes.
#Each system has a "start" function that sets up all watches.