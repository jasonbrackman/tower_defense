class Config:
    def __init__(self):
        self.__value = {"width": 320, "height": 320, "fps": 30}

        # Expected values

    def __getattr__(self, attr):
        return self.__value.get(attr)

    def __setattr__(self, attr, value):
        if attr.startswith("_"):
            object.__setattr__(self, attr, value)
        else:
            self.__value[attr] = value
