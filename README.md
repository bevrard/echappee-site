# Rouleur — Ride like a legend

Site de présentation statique de Rouleur, publié via GitHub Pages après fusion.
Le nom technique du dépôt et les URLs existantes sont conservés.

- [Application](https://legend-161af.web.app)
- [Documentation de référence](https://github.com/bevrard/legend/blob/main/docs/README.md)
- [Décision de marque et logo retenu](https://github.com/bevrard/legend/issues/4#issuecomment-6527955878)

Le contenu présente Training, Flash et Échappée d’après le code et la documentation
fonctionnelle de l’application au commit `3d7a5a4`. Les limites outdoor, matérielles
et de persistance sont explicites. Strava et le coaching restent des intentions.

## Prévisualiser

```sh
python3 -m http.server 8080
```

Ouvrir `http://localhost:8080`. Aucun build ni service payant n’est nécessaire.
La branche de rebranding ne publie pas le site en production.

## Assets : master unique

Le dessin de référence est le logo original sur fond blanc, conservé intact dans
le dépôt de l’application : [master](https://github.com/bevrard/legend/blob/main/resources/branding/master/logo-original-white.png).
SHA-256 : `fc50d71ddfbc380fab698e85c85150988bcba5439e811a25f640ebff52183066`.

Les logos et icônes du site sont des copies des exports mécaniques de l’application.
Les formes, les couleurs, les angles de la montagne, le vélo et le casque ne
doivent jamais être régénérés ou retouchés. Le fichier `assets/branding-manifest.json`
porte l’empreinte du master et les empreintes des pixels attendus.

Depuis le checkout de l’application, avec Pillow installé selon son fichier
`scripts/requirements-branding.txt` :

```sh
python3 scripts/export-branding.py --site-dir /chemin/du/site
python3 scripts/export-branding.py --check --site-dir /chemin/du/site
```

Voir le [contrat de marque](https://github.com/bevrard/legend/blob/main/docs/development/rebranding.md).
Le fichier historique `assets/lechappee-logo.png` reste conservé intact. Il ne doit
pas être modifié pour créer une nouvelle version de marque.

Le contrôle local `python3 scripts/check-branding.py` (Pillow selon
`scripts/requirements-branding.txt`) vérifie le master historique, le dessin du
logo public pixel pour pixel et les empreintes des trois exports. Le workflow
`Brand consistency checks` exécute ce contrôle sur les PR qui touchent aux assets.
