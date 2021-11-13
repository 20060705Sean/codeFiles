us3rInput = list(map(int, input().split()))

gcd = lambda a, b:gcd_factor(max(a, b), min(a,b))
gcd_factor = lambda a, b:b if a % b == 0 else gcd_factor(b, a % b)
lcm = lambda a, b:a * b / gcd(a, b)

_backslashN = "\n"
_patchZero = lambda s:s + "0" if len(s[s.index(".")+1:]) == 1 else s

a, b, c, d, e, f = us3rInput
if a==0 or b==0 or d==0 or e==0:
    x, y = 0.0, 0.0
    if (a == 0 and b == 0) or (d == 0 and e == 0):print("No answer" if c != 0 else "Too many")
    elif (a == 0 and d == 0) or (b == 0 and e == 0):print("Too many"if c * (d if e == 0 else e) == f * (a if b == 0 else b) else"No answer")
    else:
        if a == 0:y=c/b
        if b == 0:x=c/a
        if d == 0:y=f/e
        if e == 0:x=f/d
        x= round(x, 2)
        y = round(y, 2)
        print(f"x={_patchZero(str(x))}{_backslashN}y={_patchZero(str(y))}")
else:
    ratio = (lcm(a, d)/a, lcm(a, d)/d)
    a *= ratio[0]; b *= ratio[0]; c *= ratio[0]; d *= ratio[1]; e *= ratio[1]; f *= ratio[1]
    if a * e - b * d == 0:print("Too many" if c == f else "No answer")
    else:
        x=round((c * e - f * b)/(a * e - b * d), 2)
        y=round((f * a - c * d)/(a * e - b * d), 2)
        print(f"x={_patchZero(str(x))}{_backslashN}y={_patchZero(str(y))}")