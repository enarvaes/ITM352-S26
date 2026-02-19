test_cases = [
    [1, 2],
    [1, 2, 3, 4, 5, 6],
    [i for i in range(12)]
]

for test in test_cases:
    if len(test) < 5:
        print(f"Length {len(test)}: Small")
    elif 5 <= len(test) <= 10:
        print(f"Length {len(test)}: Medium")
    else:
        print(f"Length {len(test)}: Large")