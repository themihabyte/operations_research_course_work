class Solution:
    def __init__(self, T):
        self.z = 0
        self.x = []
        for i in range(T):
            self.x.append(0)

    def __str__(self):
        return "Z = {:.3f}, x = {}".format(self.z, self.x)
    
    def __eq__(self, value):
        if isinstance(value, Solution):
            if len(self.x) != len(value.x):
                return False
            for i in range(len(self.x)):
                if self.x[i] != value.x[i]:
                    return False
            if self.z != value.z:
                return False
            return True

        return NotImplemented
    
    def increase_z(self, value):
        self.z += value