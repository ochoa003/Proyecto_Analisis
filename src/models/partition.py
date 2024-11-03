# models/partition.py
from loopback import Model, property

class Partition(Model):
    id = property(str, id=True)
    subset1 = property(list, required=True)
    subset2 = property(list, required=True)
    emd_value = property(float, required=True)

    def __init__(self, data=None):
        super().__init__()
        if data:
            for key, value in data.items():
                setattr(self, key, value)