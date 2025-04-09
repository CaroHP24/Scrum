require 'time'
require 'securerandom'

start_time = Time.now

total = 0
1000.times do |i|
  1000.times do |j|
    total += (i * j + rand(0..10))
  end
end

end_time = Time.now

puts "Boucles for imbriquées :"
puts "Temps d'exécution : #{(end_time - start_time).round(2)} secondes"
puts ""

# Lecture du fichier
start_time = Time.now
contenu = File.read("FichierTest.txt", encoding: "UTF-8")
end_time = Time.now

puts "Lecture de fichier :"
puts "Lecture terminée. Taille : #{contenu.length} caractères"
puts "Temps de lecture : #{(end_time - start_time).round(2)} secondes"