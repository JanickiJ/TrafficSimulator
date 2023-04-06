import time
from statistics import mean, stdev

import pandas as pd
from matplotlib import pyplot as plt


class Measurements:
    def __init__(self, ):
        self.times = []
        self.cars_number = []
        self.average_speed = []
        self.stopped_cars = []
        self.stdev_speed = []
        self.precision = 5
        self.precision_counter = 1

    def save_step(self, time, cars):
        if self.precision % 5:
            cars = list(filter(lambda car: car.finished == False, cars))
            if not cars:
                return
            self.times.append(time)
            self.cars_number.append(len(cars))
            self.stopped_cars.append(len(list(filter(lambda car: car.v == 0, cars))))
            self.average_speed.append(mean(list(map(lambda car: car.v, cars))))
            if len(cars) > 2:
                self.stdev_speed.append(stdev(list(map(lambda car: car.v, cars))))
            else:
                self.stdev_speed.append(0)
        self.precision += 1

    def save_measurements(self, simulation_name):
        print("=== RESULTS ===")
        data = {'cars_number': self.cars_number,
                'stopped_cars': self.stopped_cars,
                'average_speed': self.average_speed,
                'stdev_speed': self.stdev_speed
                }

        df = pd.DataFrame(data, index=self.times)
        file_name = simulation_name + "-" + time.strftime("%Y_%m_%d-%H_%M_%S")
        print(file_name + ".csv")
        self.plot_stopped_cars(df, simulation_name, file_name)
        df.to_csv('./records/' + file_name)
        print(df.head(10))
        print(df.size)

    def plot_results(self, data, simulation_name, name):
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.set_title(simulation_name, loc="right")
        ax1.plot(data.index, data['average_speed'])
        ax1.fill_between(data.index, data['average_speed'] - data['stdev_speed'],
                         data['average_speed'] + data['stdev_speed'], alpha=.5)
        ax2.plot(data.index, data['cars_number'], 'g')
        fig.legend(['Average speed with std', 'Average speed STD', 'Cars number'], loc='upper left')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Average speed', color='b')
        ax2.set_ylabel('Cars number', color='g')
        plt.show()

    # plt.savefig('./images/' + name + ".png")

    def plot_stopped_cars(self, data, simulation_name, name):
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.set_title(simulation_name, loc="right")
        ax1.plot(data.index, data['stopped_cars'])
        ax2.plot(data.index, data['cars_number'], 'g')
        fig.legend(['Stopped cars', 'Cars number'], loc='upper left')
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Stopped cars', color='b')
        ax2.set_ylabel('Cars number', color='g')
        plt.show()
    # plt.savefig('./images/' + name + ".png")
