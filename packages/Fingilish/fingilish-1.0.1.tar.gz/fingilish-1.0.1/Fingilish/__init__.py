class Fn:
    def __init__(self):
        self.data = {}

    def bn(self, content):
        print(content)

    def zk(self, key, value):
        self.data[key] = value

    def zb(self, key):
        return self.data[key]

    def ag(self, condition, action):
        if condition:
            if callable(action):
                return action()
            return action

    def rk(self, content):
        return str(content)

    def ak(self, content):
        return int(content)

    def bk(self, content):
        return bool(content)

    def sk(self, content):
        return float(content)


class Finglish:
    def __init__(self):
        self.data = {}

    def benevis(self, content):
        print(content)

    def zakhire_kon(self, key, value):
        self.data[key] = value

    def zakhire_bede(self, key):
        return self.data[key]

    def agar(self, condition, action):
        if condition:
            if callable(action):
                return action()
            return action

    def reshte_kon(self, content):
        return str(content)

    def adad_kon(self, content):
        return int(content)

    def boolean_kon(self, content):
        return bool(content)

    def shenavar_kon(self, content):
        return float(content)
