# (a) Conditional expression version
emotions = ("fear", "sad", "surprise", "happy")
result = "true" if len(emotions) > 3 and emotions[-1] == "happy" else "false"
print(result)

# (b) If-statement version
if len(emotions) > 3 and emotions[-1] == "happy":
    print("true")
else:
    print("false")