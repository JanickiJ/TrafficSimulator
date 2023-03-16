import numpy as np

max_car_length = 12.5
max_vehicle_width = 3.0

def id(a) :
    return a

class Generator :

    def __init__(self, carTypes, paths, simulation, intensity_function = id) :
        self.sum = 0
        self.pathSum = 0
        self.number = 0
        self.typesWithLikelihood = []
        self.pathsWithLikelihood = []
        self.queue = []
        self.summary = {}
        self.pathSummary= {}
        self.simulation = simulation
        self.intensity_function = intensity_function
        for type in carTypes :
            self.typesWithLikelihood.append((self.sum, type[1]))
            self.sum += type[0]
        for path in paths :
            self.pathsWithLikelihood.append((self.pathSum, path[1]))
            self.pathSum += path[0]

    def chooseType(self) :
        likelihood = np.random.uniform(0, self.sum)
        a, b = 0, len(self.typesWithLikelihood)
        while(a < b - 1) :
            if(self.typesWithLikelihood[(a + b) // 2][0] < likelihood) :
                a = (a + b) // 2
            else :
                b = (a + b) // 2
        if a in self.summary.keys() :
            self.summary[a] += 1
        else :
            self.summary[a] = 1
        return a
    
    def choosePath(self) :
        likelihood = np.random.uniform(0, self.pathSum)
        a, b = 0, len(self.pathsWithLikelihood)
        while(a < b - 1) :
            if(self.pathsWithLikelihood[(a + b) // 2][0] < likelihood) :
                a = (a + b) // 2
            else :
                b = (a + b) // 2
        if a in self.pathSummary.keys() :
            self.pathSummary[a] += 1
        else :
            self.pathSummary[a] = 1
        return a

    def generateCars(self, n) :
        for _ in range(n) :
            self.number += 1
            a = self.chooseType()
            b = self.choosePath()
            carType = self.typesWithLikelihood[a][1]
            carType["id"] = self.number
            carType["path"] = self.pathsWithLikelihood[b][1]
            if self.simulation.roads[carType["path"][0]].length < 2 * max_car_length : continue
            carType["position"] = 12.0 + (self.simulation.roads[carType["path"][0]].length - 2 * max_car_length) * np.random.uniform(0.0, 1.0)
            if self.simulation.can_add_car(carType["path"][0], carType["position"], max_car_length) :
                self.simulation.set_vehicles([({}, carType)])
            else :
                self.queue.append(carType)
            # print(self.pathsWithLikelihood[b][1], carType["position"])
            # print(self.summary)

    def generate(self, simulation_time, dt) :
        new_queue = []
        for car in self.queue :
            if self.simulation.can_add_car(car["path"][0], car["position"], max_car_length) :
                self.simulation.set_vehicles([({}, car)])
            else :
                new_queue.append(car)
        self.queue = new_queue
        print(simulation_time, self.intensity_function(simulation_time) * dt, "dt =", dt)
        if np.random.uniform(0, 1.0) <= self.intensity_function(simulation_time) * dt :
            self.generateCars(1)

        