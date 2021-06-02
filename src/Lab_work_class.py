class Lab_work:
    def __init__(self, p, n):
        self.p = p
        self.n = n
        self.P = []
        self.__calculate_probability_for_try()
    
    def __calculate_probability_for_try(self):
        for i in range(self.n+1):
            if i == 0:
                self.P.append(0)
            else:
                self.P.append(1-(1-self.p)**(i))