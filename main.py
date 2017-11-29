import sys

class App(object):
    def __init__(self, max):
        self.table = [[0 for k in range(max + 1)] for n in range(max + 1)]
        self.max = max

    def build(self):
        for n in range(self.max + 1):
            for k in range(self.max + 1):
                if k == 0:      b = 1
                elif  k > n:    b = 0
                elif k == n:    b = 1
                elif k == 1:    b = n
                elif k > n-k:   b = self.table[n][n-k]
                else:
                    b = self.table[n-1][k] + self.table[n-1][k-1]
                self.table[n][k] = b

    def output(self, val):
        if val > 2**63: val = -1
        text = " {0}LL,".format(val)

        if self.column + len(text) > 76:
            print("\n   ", end = "")
            self.column = 3
        print(text, end = "")
        self.column += len(text)

    def dump(self):
        count = 0
        print("long long bctable[] = {", end="");

        self.column = 999
        for n in range(self.max + 1):
            for k in range(self.max + 1):
                if n < 4 or k < 2 or k > n-k:
                    continue
                self.output(self.table[n][k])
                count += 1
        print("\n}}; /* {0} Entries */".format(count));

    def run(self):
        self.build()
        self.dump()
        return 0

def main(args):
    return App(54).run()

if __name__ == "__main__":
    sys.exit(main(sys.argv))