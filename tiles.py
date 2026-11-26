
from pathlib import Path
import geopandas as gpd
import subprocess
import numpy as np
import folium
import mapclassify

# Chemin des données
data_path = "902-1-tp-communes/donnees"

# Chargement des données geojson
df_comm = gpd.read_file(Path(data_path, "communes_64_65.gpkg"), layer='communes')    # on utilise le contour précis pour calculer l'aire dans le coeur
df_comm_p = gpd.read_file(Path(data_path, "communes_64_65.gpkg"), layer='communes_precis')    # on utilise le contour précis pour calculer l'aire dans le coeur
df_aire = gpd.read_file(Path(data_path, "pnp_aire_adhesion.geojson"))
df_coeur = gpd.read_file(Path(data_path, "pnp_coeur.geojson"))
print(f'Nb de communes: {len(df_comm)}')

# Changement de SCR des geojson 4326 -> 2154
df_aire = df_aire.to_crs("EPSG:2154")
df_coeur = df_coeur.to_crs("EPSG:2154")

# On recalcule l'aire des communes
df_comm_p['surface_m2'] = df_comm_p.area

# Détermination des communes ayant du territoire dans le PNP
# Jointure spatiale: communes et aire adhésion
df_comm_pnp = df_comm_p.sjoin(df_aire, how='inner', predicate='intersects')
df_comm_pnp = df_comm_pnp.drop(columns=['index_right', 'nom_right'])
print(f"Nb de communes dans l'aire d'adhésion: {len(df_comm_pnp)}")
# Calcul de la part se situant dans le coeur du PNP
# Jointure spatiale entre communes dans aire PNP et coeur PNP (on garde toutes les communes)
df_comm_coeur = gpd.overlay(df_comm_pnp, df_coeur, how='intersection')
# Cacul de l'aire
df_comm_coeur['surface_m2_coeur'] = df_comm_coeur.area
df_comm_coeur['part_surf_coeur'] = df_comm_coeur['surface_m2_coeur']/df_comm_coeur['surface_m2']*100
df_comm_coeur['part_surf_coeur'] = df_comm_coeur['part_surf_coeur'].astype('float32')
df_comm_coeur = df_comm_coeur.drop(columns=['nom_left', 'surface_m2', 'surface_m2_coeur', 'nom', 'geometry'])
print(f"Nb de communes dans le coeur: {len(df_comm_coeur[df_comm_coeur['part_surf_coeur'] > 0])}")

# Jointure attributaire pour ajouter la colonne 'part_surf_coeur' à la couche communes
# on ne garde que les communes qui intersectent le pnp
df_comm = df_comm[df_comm['code_insee'].isin(df_comm_pnp['code_insee'])]
df_comm = df_comm.merge(df_comm_coeur, on='code_insee', how="left")
df_comm["part_surf_coeur"] = df_comm["part_surf_coeur"].fillna(0)
df_comm.explore().save("communes.html")


# Sauvegarde dans un fichier geoson (conversion SCR)
df_comm = df_comm.to_crs("EPSG:4326")

# Construction des tuiles vectorielles
data_path_gpkg = Path(data_path, "parc.gpkg")
data_path_pmtiles = Path(data_path, "parc.pmtiles")
data_path_gpkg.unlink(missing_ok=True)
data_path_pmtiles.unlink(missing_ok=True)

df_comm.to_file(data_path_gpkg, layer='communes')
df_aire.to_file(data_path_gpkg, layer='aire')
df_coeur.to_file(data_path_gpkg, layer='coeur')

subprocess.run([
    "ogr2ogr", "-f", "PMTiles", data_path_pmtiles, data_path_gpkg,
    "-dsco", "MINZOOM=6", "-dsco", "MAXZOOM=14", "-preserve_fid"], check=True) 
