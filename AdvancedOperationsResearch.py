# info = Shanghai Jiao Tong University, Cao Jinhao, 122010910216
from itertools import combinations
import random
import pulp as p

class AdvancedOperationsResearch(object):
    # date = 2022/10/09
    def Assignment1Question1():
        # objective = max
        m = p.LpProblem("how much of each product Omega should produce", p.LpMaximize)

        # xi >= 0, x3 <= 20 and xi is integer
        x1 = p.LpVariable("x1", 0, None, p.LpInteger)
        x2 = p.LpVariable("x2", 0, None, p.LpInteger)
        x3 = p.LpVariable("x3", 0, 20, p.LpInteger)

        # add objective
        m += 50 * x1 + 20 * x2 + 25 * x3

        # add constraint for milling machine
        m += 9 * x1 + 3 * x2 + 5 * x3 <= 500

        # add constraint for lathe
        m += 5 * x1 + 4 * x2 + 0 * x3 <= 350

        # add constraint for milling grinder
        m += 3 * x1 + 0 * x2 + 2 * x3 <= 150

        m.solve()
        for v in m.variables():
            print("%s=%s"%(v.name, int(v.varValue)))

    # date = 2022/10/12
    def GenerateCoordinate(N):
        # (int) x or y >=0
        # (int) x or y < 100
        a = [[random.randint(0, 100) for j in range(2)] for i in range(N)]
        return a

    def Coordinate2Distance(Coordinate):
        L = len(Coordinate)
        # fill with 0
        Distance =  [[0 for i in range(L)] for j in range(L)]
        for FromIndex, FromItem in enumerate(Coordinate):
            for ToIndex, ToItem in enumerate(Coordinate):
                if FromIndex < ToIndex:
                    FromX = FromItem[0]
                    FromY = FromItem[1]
                    ToX = ToItem[0]
                    ToY = ToItem[1]
                    Distance[FromIndex][ToIndex] = ( (ToX - FromX) ** 2 + (ToY - FromY) ** 2) ** 0.5
                elif FromIndex > ToIndex:
                    # flip the matrix => for example: a[2][1] = a[1][2]
                    Distance[FromIndex][ToIndex] = Distance[ToIndex][FromIndex]
        return Distance

    # date = 2022/10/12
    def Assignment1Question2Method1(C):
        # get number of cities
        n = len(C)

        # get set of cities
        N = range(n)

        # edges = (i, j) for i != j
        E = [(i, j) for i in N for j in N if i != j]

        # objective = min
        m = p.LpProblem("TSP", p.LpMinimize)

        # create variables
        x = p.LpVariable.dicts("x", E, None, None, p.LpBinary)

        # add objective
        m += sum([C[i][j] * x[(i, j)] for (i, j) in E])

        # add constraints
        for i in N:
            m += sum([x[(i, j)] for j in N if i != j]) == 1
            m += sum([x[(j, i)] for j in N if i != j]) == 1

        m.solve()

        # collect objective and solution
        vobj = p.value(m.objective)
        xsol = { e: p.value(x[e]) for e in E }

        # find a subtour from city 0
        def subtour(xsol):
            succ = 0
            subt = [ succ ]
            while True:
                succ = sum(xsol[succ, j] * j for j in N if j != succ)
                if succ == 0:
                    break
                subt.append(int(succ))
            return subt

        # add subtour elimination constraints
        while True:
            subt = subtour(xsol)
            if len(subt) == n:
                print("Optimal tour found: %s"%subt)
                print("Optimal tour length: %s"%vobj)
                break
            print("Subtour found: %s"%subt)

            m += sum([x[(i, j)] for i in subt for j in subt if i != j]) <= len(subt) - 1

            m.solve()
            vobj = p.value(m.objective)
            xsol = { e: p.value(x[e]) for e in E }

    # date = 2022/10/24
    # get all subtours
    def CombineSubtour(N1, n):
        N2 = []
        for c in combinations(N1, n):
            N2.append(c)
        return N2

    # date = 2022/10/24
    def Assignment1Question2Method2(C):
        # get number of cities
        n = len(C)

        # get set of cities
        N = range(n)

        # edges = (i, j) for i != j
        E = [(i, j) for i in N for j in N if i != j]

        # objective = min
        m = p.LpProblem("TSP", p.LpMinimize)

        # create variables
        x = p.LpVariable.dicts("x", E, None, None, p.LpBinary)

        # add objective
        m += sum([C[i][j] * x[(i, j)] for (i, j) in E])

        # add constraints
        for i in N:
            m += sum([x[(i, j)] for j in N if i != j]) == 1
            m += sum([x[(j, i)] for j in N if i != j]) == 1

        # add extra constraints
        subts = []
        for i in range(2, n):
            subts.extend(AdvancedOperationsResearch.CombineSubtour(range(n), i))
        # print(subts)

        for subt in subts:
            m += sum([x[(i, j)] for i in subt for j in subt if i != j]) <= len(subt) - 1

        m.solve()

        print("Optimal tour length: %s"%p.value(m.objective))

        # A to B, C to A, бн
        vobj = []
        for (i, j) in E:
            if p.value(x[(i, j)]) > 0:
                vobj.append((i, j))
        # print for test
        # print(vobj)

        # C to A to B to бн (Start from node 0)
        subt = []
        for i in vobj:
            if (i[0] == 0):
                subt.append(i[0])
                subt.append(i[1])
                break

        # imply the process of bubble sort
        for n in vobj:
            for i in vobj:
                if (i[0] == subt[-1] and i[1] != 0):
                    subt.append(i[1])
        print("Optimal tour found: %s"%subt)


       

if __name__ == "__main__":
    #AdvancedOperationsResearch.Assignment1Question1()

    # C0 is an example from class
    C0 = [[0, 86, 49, 47,90,90,50],
            [86,0,68,79,93,24,5],
            [49,68,0,16,7,72,67],
            [57,79,16,0,90,69,1],
            [31,93,7,90,0,86,59],
            [69,24,72,69,86,0,81],
            [50,5,67,1,2,81,0]]

    Coordinate = AdvancedOperationsResearch.GenerateCoordinate(50) # 5, 6, 7, 8, бн, 14, 20

    Distance = AdvancedOperationsResearch.Coordinate2Distance(Coordinate)
    AdvancedOperationsResearch.Assignment1Question2Method1(Distance)
    AdvancedOperationsResearch.Assignment1Question2Method2(Distance)










