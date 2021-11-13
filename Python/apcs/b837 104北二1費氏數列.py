fbs = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040]
time = int(input())
for i in range(time):
    mini, maxi = list(sorted(list(map(int, input().split()))))
    sup, inf = -1, -1
    for i in fbs:
        if mini < i:
            inf = i
    for i in list(reversed(fbs)):
        if maxi > i:
            sup = i
    for i in range(fbs.index(inf), fbs.index(sup)):
        print(fbs[i])
    print(fbs.index(sup) - fbs.index(inf))
    print("------")
