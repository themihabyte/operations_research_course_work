class Solution:
    def __init__(self, T):
        self.z = 0
        self.x = []
        for i in range(T):
            self.x.append(0)

    def __str__(self):
        return "Z = {:.3f}, x = {}".format(self.z, self.x)