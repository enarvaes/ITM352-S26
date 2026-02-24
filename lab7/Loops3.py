health = 100

while health > 0:
    print(f"current health: {health}")
    damage = int(input("Enter the damage taken: "))
    health -= damage

print("Game Over!")
