#!/usr/bin/env python
# https://stackoverflow.com/questions/46438288/how-do-i-implement-this-function-in-python-2-7-using-inheritance

# Python inheritance demo


class Car(object):
    def __init__(self, wheels, miles, make, model, year):
        self.wheels = wheels   #number of wheels
        self.miles = miles     #number of miles
        self.make = make       #manufactorers
        self.model = model     #model
        self.year = year       #year
        self.sold_for = 0      #0 if it is not sold. Money obtained otherwise
        self.base_price= float(20000) #price for a new car, the same for every car.

    def set_sold_for(self,amount):
        self.sold_for = amount

    def price_on_market(self):
        return self.base_price - (.10 * self.miles)

    def print_dealer_status(self):
        if int(self.sold_for) == 0:
            sold_status = "not sold"
        else:
            sold_status = self.sold_for
        status_dict = {'make': self.make,
        'model': self.model,
        'price_on_market': self.price_on_market(),
        'sold_for': sold_status}
        print(status_dict)



class Pickup(Car):
    def __init__(self,load_capacity, *args, **kwargs):
        Car.__init__(self, *args, **kwargs)
        self.sold_for = 0    #0 if it is not sold. Money obtained otherwise
        self.load_capacity=float(load_capacity) #load capacity (can be 1, 0.75 or 0.5)
        self.base_price= float(35000) #price for a new pickup, the same for every pickup.


    def price_on_market(self):
        return self.base_price - (.10 * float(self.miles)) + (float(self.load_capacity) * 5000)


class Motorbike(Car):
    def __init__(self, *args, **kwargs):
        Car.__init__(self, *args, **kwargs)
        self.sold_for = 0    #0 if it is not sold. Money obtained otherwise
        self.base_price= float(10000) #price for a new motorbike, the same for every motorbike.

    def price_on_market(self):
        return self.base_price - (.30 * self.miles)




car1 = Car(wheels = 4, miles = 10000, make = "Ford", model = "Focus", year = 2013)
car2 = Car(wheels = 4, miles = 12000, make = "Nissan", model ="Altima", year = 2015)

moto1 = Motorbike(wheels = 2, miles = 5000, make = "Triumph", model = "Boneville", year = 2015)
moto2 = Motorbike(wheels = 2, miles = 3000, make = "Ducati", model = "Hypermotard", year = 2013)

pickup = Pickup(wheels = 4, miles = 8000, make = "Chevrolet", model = "Silverado", year = 2010, load_capacity = 0.5)

carDealer = [car1,car2,moto1,moto2,pickup]


car1.set_sold_for(17000)
moto2.set_sold_for(11000)

for car in carDealer:
    car.print_dealer_status()
