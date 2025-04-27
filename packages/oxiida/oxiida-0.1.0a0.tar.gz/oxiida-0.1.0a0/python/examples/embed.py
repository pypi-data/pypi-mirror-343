# example showing foreign function interface rs <-> py
import oxiida
from time import sleep, time

xx = 4
yy = 6
y = 88

def py_plus(lhs: float, rhs: float) -> float:
    print(f"here is x: {xx}")
    return lhs + rhs

print(py_plus(xx, yy))

# language = oxiida
workflow = """
require py_plus;
require time, sleep;

para {
    print "--anchor--";
    print time();
    seq {
        sleep(2);
        print time();
    }

    seq {
        sleep(2);
        print time();
    }
}

seq {
    print "--anchor--";
    print time();
    seq {
        sleep(2);
        print time();
    }

    seq {
        sleep(2);
        print time();
    }
}

y = 7;
print py_plus(10, y);
"""

if __name__ == '__main__':
    oxiida.run(workflow)
