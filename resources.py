class Resources:
    def __init__(self, w=0, g=0, p=0):
        self.w = w
        self.g = g
        self.p = p

    def __add__(self, other):
        assert(type(other) == Resources)
        return Resources(self.w + other.w, self.g + other.g, self.p + other.p)

    def __sub__(self, other):
        assert(type(other) == Resources)
        return Resources(self.w - other.w, self.g - other.g, self.p - other.p)

    def __mul__(self, other):
        if type(other) == int:
            return Resources(self.w * other, self.g * other, self.p * other)

        assert(type(other) == Resources)
        return Resources(self.w * other.w, self.g * other.g, self.p * other.p)

    def __str__(self):
        return f'Resources(w={self.w}, g={self.g}, p={self.p})'

    def __repr__(self):
        return self.__str__()

    def copy(self):
        return Resources(w=self.w, g=self.g, p=self.p)
