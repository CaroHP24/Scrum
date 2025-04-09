import time
import random

start1=time.time()

total=0
for i in range(1000):
    for j in range(1000):
            total += (i * j + random.randint(0, 10))

end1 = time.time()





start2 = time.time()

with open("FichierTest.txt", "r", encoding="utf-8") as f:
    contenu = f.read()

print(contenu)
end2 = time.time()


print(f"Résultat final : {total}")
print(f"Temps d'exécution : {end1 - start1:.2f} secondes")

print(f"Lecture terminée. Taille : {len(contenu)} caractères")
print(f"Temps de lecture : {end2 - start2:.2f} secondes")




