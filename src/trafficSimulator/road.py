from scipy.spatial import distance


class Road:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = distance.euclidean(self.start, self.end)
        self.angle_sin = (self.end[1] - self.start[1]) / self.length
        self.angle_cos = (self.end[0] - self.start[0]) / self.length
