from dataclasses import dataclass
from scipy import optimize
from math import sin, cos

@dataclass()
class Case:
    name: str
    func: str
    x_0: str
    expected: float

    def __str__(self) -> str:
        return 'test_{}'.format(self.name)


# TESTS_NUMBER = 5
TESTS_NUMBER = 6
FUNCTIONS = ["x**2 + y**2",
             "x**2 + y**2 + z**2",
             "2 * (x - y + z) - k * 3 + 14 * x**2 - 12 * y**3",
             "x**2 + y - z + k",
             "cos(x) + sin(x)",
             "(x**2 + y - 11)**2 + (x + y**2 - 7)**2 - 5"]  # димин тест

LAMBDAS = [lambda x: x[0]**2 + x[1]**2, lambda x: x[0]**2 + x[1]**2 + x[3]**2,
           lambda x: 2 * (x[0] - x[1] + x[2]) - 3 * x[3] + 14*x[0]**2 - 12 * x[1]**3,
           lambda x: x[0]**2 + x[1] - x[2] + x[3],
           lambda x: sin(x) + cos(x), lambda x: (x[0]**2 + x[1] - 11)**2 + (x[0] + x[1]**2 - 7)**2 - 5]

X_0 = [{'x': 0, 'y': 12.1},
       {'x': 0.5, 'y': 130, 'z': -51},
       {'x': 0.9, 'y': 12.1, 'z': -34.5, 'k': 2.},
       {'x': -2.9, 'y': 2.1, 'z': 34.5, 'k': 22.},
       {'x': 11.},
       {'x': 0.0, 'y': 0.0}]  # димин тест


EXPECTED = [0.0,
            0.0,
            11111.,  # минимизация не определена , пока так работаем
            11111.,  # минимизация не определена , пока так работаем
            -1.4141,
            -5.
            ]


def create_test_cases() -> list:
    cases = []
    for i in range(TESTS_NUMBER):
        name = "case" + str(i)
        x_0 = X_0[i]
        func = FUNCTIONS[i]
        expected = EXPECTED[i]
        cases.append(Case(name, func, x_0, expected))
    return cases
