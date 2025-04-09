import time
import random

start=time.time()

total=0
for i in range(1000):
    for j in range(1000):
            total += (i * j + random.randint(0, 10))

end = time.time()

print(f"Résultat final : {total}")
print(f"Temps d'exécution : {end - start:.2f} secondes")



start = time.time()

with open("FichierTest.txt", "r", encoding="utf-8") as f:
    contenu = f.read()

end = time.time()

print(f"Lecture terminée. Taille : {len(contenu)} caractères")
print(f"Temps de lecture : {end - start:.2f} secondes")




