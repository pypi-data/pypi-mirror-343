from tpltable.basic import *


class UnitCell:
    def __init__(self, value, style):
        self.value = value
        self.style = style

    def __str__(self):
        return str(self.value)


