import threading
import time
import os
class Main:
    def __init__(self):
        self.activities = []
        self.objects = []
    def start(self):
        for function in self.activities:
            def f():
                function.run()
            p = threading.Thread(target = f, args=())
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
    system1.attach(system2.__class__.__name__,system2)
    system2.attach(system1.__class__.__name__,system1)
class System:
    def __init__(self):
        self.watches = {}
        main.activities.append(self)
    def __setattr__(self,attr,value):
        self.__dict__[attr] = value
        """for function in [a for a in dir(self) if not a.startswith('__')]:
            try:
                if getattr(self,function).watch[0] == attr:
                    value.observe(getattr(self,function).watch[1],getattr(self,function))
            except AttributeError:
                pass"""
        self.notify(attr)
    def attach(self,attr,value):
        try:
            self.__dict__[attr].append(value)
        except (KeyError,AttributeError):
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
class Object(System):
    def __init__(self,x,y,z,name):
        System.__init__(self)
        main.objects.append(self)
        self.cargoes = []
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0
        self.ax = 0
        self.ay = 0
        self.az = 0
        self.name = name
        self.counter = 0
    def activity(self):
        self.x += self.vx*self.delta + 0.5*self.ax*self.delta*self.delta
        self.y += self.vy*self.delta + 0.5*self.ay*self.delta*self.delta
        self.z += self.vz*self.delta + 0.5*self.az*self.delta*self.delta
        self.vx = self.vx + self.ax*self.delta
        self.vy = self.vy + self.ay*self.delta
        self.vz = self.vz + self.az*self.delta
        self.counter += 1
    def test(self,x):
        self.x = x
    def damage(self,factor):
        pass
class Shuttle(Object):
    def __init__(self,x,y,z,name):
        Object.__init__(self,x,y,z,name)
        self.location = None
    def activity(self):
        if self.location != None:
            self.x = self.location.x
            self.y = self.location.y
            self.z = self.location.z
            #self.vx = 0
            self.vy = 0
            self.vz = 0
            self.ax = 0
            self.ay = 0
            self.az = 0
        else:
            Object.activity(self)
    def dock(self,location):
        if self.location != None:
            return "Detach first."
        if distance(self,location) < 50*50:
            self.location = location
            self.location.cargoes.append(self)
            return True
        return "Distance too far."
    def undock(self):
        print("undocking")
        self.location.cargoes.remove(self)
        self.location = None
        print(self.location)
class Cargo(System):
    def __init__(self,location,name):
        System.__init__(self)
        self.cargoes = []
        self.location = location
        self.location.cargoes.append(self)
        self.name = name
    def transfer(self,location):
        if distance(self.location,location) < 50*50:
            self.location.cargoes.remove(self)
            self.location = location
            self.location.cargoes.append(self)
            return True
        return "Distance too far."
def distance(l1,l2):
    try:
        xl1 = l1.x
        yl1 = l1.y
        zl1 = l1.z
    except AttributeError:
        return distance(l1.location,l2)
    try:
        xl2 = l2.x
        yl2 = l2.y
        zl2 = l2.z
    except AttributeError:
        return distance(l1,l2.location)
    return (xl2-xl1)*(xl2-xl1)+(yl2-yl1)*(yl2-yl1)+(zl2-zl1)*(zl2-zl1)
class Ship(Object):
    def __init__(self,x,y,z,callsign,nation):
        Object.__init__(self,x,y,z,callsign)
        self.nation = nation
    def damage(self,factor):
        pass
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
        if status == True and self.Repair.course > 50:
            self.status = True
            return True
        if status == True:
            return "System damaged."
        if status == False:
            self.status = False
            return True
    @watch("Repair","course")
    def damage_changed(self):
        if self.Repair.course < 50:
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
        self.x = 0
        self.y = 0
        self.z = 0
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
        self.SecurityTeam = []
class SecurityTeam(Cargo):
    def __init__(self,location,name):
        Cargo.__init__(self,location,name)
        self.status = 0 #Standing By
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
#ship = Ship(0,0,0,"Enterprise","USS")
#ship2 = Ship(0,49.9,0,"Enterprise2","USS")
#c1 = Cargo(ship,"Engine Room")
#c2 = Cargo(ship,"Shuttle Bay 1")
#s1 = Security()
#s2 = SecurityTeam(c1,"Team1")
#s3 = Shuttle(0,0,0,"Shuttle1")
#s3.dock(ship)
#attach(s2,s1)
#attach(s1,ship)
#ship.Security.SecurityTeam[0].transfer(s3)
#print(ship.Security.SecurityTeam[0].location.name)
#s3.undock()
#print(s3.location)
#s3.vx = 1000
#time.sleep(5)
#print(s3.x)
#s3.vx = 0
#ship.Security.SecurityTeam[0].transfer(c1)
#print(ship.Security.SecurityTeam[0].location.name)
#How to handle power?
#main.start()
#Each system stores other systems it needs as attributes.
#Each system has a "start" function that sets up all watches.