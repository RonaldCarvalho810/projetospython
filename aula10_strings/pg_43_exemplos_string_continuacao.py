import os
os.system("cls")

print("=" *20)
print("funções string")
print("=" *20)

frase1 = "Olá Mundo!"
quantidade_caracteres = len(frase1)
print(f"A frase : {frase1} \n contém {quantidade_caracteres} caracteres")
print("=" *20)

minusculas = frase1.lower()
print(f"frase original.: {frase1}")
print(f"frase nova.: {minusculas}")
print("=" *20)

maiusculas = frase1.upper()
print(f"frase original.: {frase1}")
print(f"frase nova.: {maiusculas}")
print("=" *20)

capitalizada = frase1.capitalize()
print(f"frase original.: {frase1}")
print(f"frase nova.: {capitalizada}")
print("=" *20)

frase2 = "    Olá Mundo    "
sem_espaco = frase2.strip()
print(f"frase original.: {frase2}")
print(f"frase nova.: {sem_espaco}")
print("=" *20)

substituicao = frase1.replace("Mundo", "Phyton")
print(f"frase original.: {frase1}")
print(f"frase nova.: {substituicao}")
print("=" *20)