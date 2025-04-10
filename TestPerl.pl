#!/usr/bin/perl
use strict;
use warnings;
use Time::HiRes qw(time);  #pour mesurer le temps avec une meilleure précision
use POSIX qw(strftime);  #pour obtenir un format de date si nécessaire
use List::Util qw(shuffle);

my $start_time = time();

# test de boucle imbriquée (1000*1000) avec calcul et random
my $total = 0;
for my $i (0..999) {
    for my $j (0..999) {
        $total += ($i * $j + int(rand(11)));  # intégrer nb aléatoire de 0 à 10
    }
}
my $end_time_loops = time();
print "Résultat final: $total\n";
print "Temps d'exécution pour les boucles (1000*1000): " . ($end_time_loops - $start_time) . " sec\n";

# test d'ouverture et lecture d'un fichier texte
my $start_time_read = time();
open my $fh, '<', 'FichierTest.txt' or die "Erreur : $!\n";
my $content = do { local $/; <$fh> };  # Lire tout le contenu du fichier
close $fh;

my $end_time_read = time();
print "Lecture terminée. Taille: " . length($content) . " caractères\n";
print "Temps: " . ($end_time_read - $start_time_read) . " sec\n";
