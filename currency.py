class Currency:
    def __init__(self, name: str, char_code: str, value: float):
        self.name = name
        self.char_code = char_code
        self.value = value

    def __str__(self):
        return '{} ({}): {} руб.'.format(self.name, self.char_code, self.value)
