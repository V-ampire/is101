class A:
    def test_a(self, p):
        print(f'A.test_a with {p}')

    def test(self, p):
        print(f'A.test with {p}')


class B:
    def __init__(self, registry):
        self.a = A()
        self.registry = registry

    def test(self, p):
        print(f'B.test with {p}')
        self.registry.append(p)

    def __getattr__(self, attr):
        if not attr in dir(self):
            return getattr(self.a, attr)
        return getattr(self, attr)


class C:
    registry = []
    def get_b(self):
        return B(self.registry)