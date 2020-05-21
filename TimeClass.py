class Time:
    def __init__(self, sec=0):
        self.sec = sec

    def __str__(self):
        if self.sec < 60:
            return f"{self.sec} сек"
        elif self.sec < 3600:
            return f"{self.sec // 60} мин {self.sec % 60} сек"
        else:
            return f"{self.sec // 3600} ч {self.sec % 3600 // 60} мин {self.sec % 60} сек"

    def __repr__(self):
        return str(self.sec)

    def __add__(self, other):
        if type(other) is int:
            return Time(self.sec + other)
        if type(other) is float:
            return Time(self.sec + int(other))
        elif type(other) is Time:
            return Time(self.sec + other.sec)

    def __sub__(self, other):
        if type(other) is int:
            return Time(self.sec - other)
        if type(other) is float:
            return Time(self.sec - int(other))
        elif type(other) is Time:
            return Time(self.sec - other.sec)

    def __lt__(self, other):
        if type(other) is Time:
            return self.sec < other.sec

    def __gt__(self, other):
        if type(other) is Time:
            return self.sec > other.sec
