import numpy as np

class Generator :

    def __init__(self, carTypes, simulation) :
        self.sum = 0
        self.number = 0
        self.typesWithLikelihood = []
        self.simulation = simulation
        for type in carTypes :
            self.typesWithLikelihood.append((self.sum, type[1]))
            self.sum += type[0]

    def generateCars(self, n) :
        carTypes = []
        summary = {}
        for _ in range(n) :
            self.number += 1
            likelihood = np.random.uniform(0, self.sum)
            a, b = 0, len(self.typesWithLikelihood)
            while(a < b - 1) :
                if(self.typesWithLikelihood[(a + b) // 2][0] < likelihood) :
                    a = (a + b) // 2
                else :
                    b = (a + b) // 2
            if a in summary.keys() :
                summary[a] += 1
            else :
                summary[a] = 1
            carType = self.typesWithLikelihood[a][1]
            carType["id"] = self.number
            carTypes.append(({}, carType))
            print(summary)
        self.simulation.set_vehicles(carTypes)

        