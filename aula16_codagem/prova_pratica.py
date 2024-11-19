import os
os.system("cls")

total = 0
for principal in range(1,6):
    for interno1 in range(1,6):
        total = principal*interno1
        print(total, end=" ")
    print()

# for principal in range(1, 6):
#     for interno1 in range(1, principal + 1):
#         print(interno1, end="")
#     for interno1 in range(principal - 1, 0, -1):
#         print(interno1, end="")
#     print()

# for teste in range(100,0,-1):
#     print(teste)