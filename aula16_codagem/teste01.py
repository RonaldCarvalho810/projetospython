import os

os.system("cls")

#print(list(range(2,100+1,2)))

# soma = 0
contador = 0
divisor = 0
# for principal in range(1,100+1):
#     if(principal %2 ==0):
#         print(principal, end= "-")
#         soma += principal
#         contador +=1
    
#     else:
#         continue
# print(soma)
# print(contador)

for principal in range(0,100+1):
    divisor=0
    for interno1 in range(1,principal+1):
        if(principal%interno1 == 0):
            divisor +=1
    if (divisor ==2):
        print(f"o numero.: {principal} é um numero primo")