from loopback import Model, property

class Node(Model):
    id = property(str, id=True)
    name = property(str, required=True)
    time_step = property(int, required=True)

    def __init__(self, data=None):
        super().__init__()
        if data:
            for key, value in data.items():
                setattr(self, key, value)
