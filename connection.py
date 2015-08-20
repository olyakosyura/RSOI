class InfoConnect:
    def __init__(self, login_str, code_str):
        self.login = login_str
        self.code = code_str

    def __eq__(self, other):
        return self.login == other.login and self.code == other.code


class Connect:
    def __init__(self):
        self.Connect = []

    def add(self, item):
        self.Connect.append(item)

    def remove(self, login, code):
        for element in self.Connect:
            if element.login == login and element.code == code:
                self.Connect.remove(element)
                return True

        return False

    def find(self, item):
        for element in self.Connect:
            if element == item:
                return True

        return False