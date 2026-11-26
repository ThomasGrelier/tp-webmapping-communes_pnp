# Choix
- Les communes conservées sont celles qui intersectent, au sens de chevaucher ou être contenu, l'aire puis le coeur.
Une commune qui touche n'est pas conservée. 
La géométrie précise des communes a été utilisée pour éviter les erreurs.


# Contrôles
- Vérifier que le nombre de villes dans l'aire d'adhésion est inférieur au nombre total de villes. Puis vérifier que le nombre de villes dans le coeur est inférieur à celui dans l'aire. 
- A la fin, vérifier visuellement sur la carte que toutes les villes sont correctement sélectionnées.
- Vérifier visuellement que la part de territoire qui se situe dans le parc est approximativement correcte.
- Vérifier que la part est strictement supérieure à zéro.
- Vérifier que le nombre d'habitants affiché correspond à celui qui se trouve dans le fichier communes_64_65.gpkg

# Limites
- Le contour du coeur ajouté se superpose grossièrement à celui du fond IGN.

# Journal de bord

Erreurs commises: 
- oubli de mettre de reprojeter le SCR des couches PNP dans le SCR des communes 2154--> pas d'intersection entres les couches
- utilisation des limites grossières des communes pour calculer l'aire --> proportion approximative calculée
- jointure spatiale au lieu d'intersection -> mauvaise gémoétrie dans la jointure
