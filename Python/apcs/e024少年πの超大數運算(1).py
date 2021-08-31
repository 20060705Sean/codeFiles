while True:
    dijitaru = tuple(map(int, input().split()))
    if dijitaru != (0, 0):
        print(dijitaru[0] ** dijitaru[1])
    else:
        break