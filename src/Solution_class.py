class Solution:
    labs = []
    def __init__(self, T):
        self.z = 0
        self.x = []
        for i in range(T):
            self.x.append(0)

    def calculate_z(self):
        if len(self.labs) == 0:
            return 0
        self.z = 0
        for i in range(len(self.labs)):
            for j in range(self.x[i]+1):
                self.z += self.labs[i].P[j]


    def __str__(self):
        return "Z = {:.3f}, x = {}".format(self.z, self.x)
    
    def __eq__(self, value):
        if isinstance(value, Solution):
            if len(self.x) != len(value.x):
                return False
            for i in range(len(self.x)):
                if self.x[i] != value.x[i]:
                    return False
            return True

        return NotImplemented

    def __lt__(self, value):
        return self.z < value.z

    def __le__(self, value):
        return self.z <= value.z

    def __gt__(self, value):
        return self.z > value.z

    def __ge__(self, value):
        return self.z >= value.z