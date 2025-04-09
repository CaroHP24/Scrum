#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main() {
    // Initialisation du g�n�rateur al�atoire
    srand(time(NULL));

    // === Test de calculs avec boucles et random ===
    printf("== Boucles avec op�rations al�atoires ==\n");

    clock_t start = clock();

    long long total = 0;
    for (int i = 0; i < 1000; i++) {
        for (int j = 0; j < 1000; j++) {
            total += (i * j + (rand() % 11)); // entre 0 et 10
        }
    }

    clock_t end = clock();
    double elapsed = (double)(end - start) / CLOCKS_PER_SEC;

    printf("R�sultat final : %lld\n", total);
    printf("Temps d'ex�cution : %.2f secondes\n\n", elapsed);

    // === Test de lecture de fichier entier ===
    printf("== Lecture compl�te du fichier ==\n");

    start = clock();

    FILE *f = fopen("FichierTest.txt", "rb"); // lecture binaire pour �viter les probl�mes d'encodage
    if (!f) {
        perror("Erreur d'ouverture de FichierTest.txt");
        return 1;
    }

    // Aller � la fin pour conna�tre la taille
    fseek(f, 0, SEEK_END);
    long taille = ftell(f);
    rewind(f); // retour au d�but

    // Allouer un buffer et lire le fichier
    char *contenu = malloc(taille + 1);
    if (!contenu) {
        perror("Erreur d'allocation m�moire");
        fclose(f);
        return 1;
    }

    fread(contenu, 1, taille, f);
    contenu[taille] = '\0'; // terminer proprement

    fclose(f);

    end = clock();
    elapsed = (double)(end - start) / CLOCKS_PER_SEC;

    printf("Lecture termin�e. Taille : %ld caract�res\n", taille);
    printf("Temps de lecture : %.2f secondes\n", elapsed);

    free(contenu);
    return 0;
}
