# Rouleur — Ride like a legend

Site de présentation statique de Rouleur, publié via GitHub Pages après fusion.
Le nom technique du dépôt et les URLs existantes sont conservés.

- [Application](https://legend-161af.web.app)
- [Shop Rouleur](https://shop.rouleur.club) : boutique Shopify liée depuis la navigation et le pied de page du site public. La connexion DNS et la publication de la boutique se gèrent séparément dans Shopify et chez le gestionnaire DNS.
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

## Référencement naturel (SEO)

L’optimisation répond à [legend#156](https://github.com/bevrard/legend/issues/156)
pour ce site vitrine. Le domaine de référence est `https://rouleur.club/`, défini
par [CNAME](CNAME).

État implémenté :

- [index.html](index.html) fournit un titre et une description en français,
  une URL canonique absolue, des métadonnées Open Graph et Twitter avec le logo
  approuvé, et des données structurées JSON-LD `WebSite` et `WebPage`.
- Le H1 décrit les courses cyclistes sur vélo indoor et appartient au contenu
  principal. Les dimensions intrinsèques des images réservent leur espace.
- [robots.txt](robots.txt) autorise l’exploration et déclare le
  [sitemap](sitemap.xml), qui contient la page d’accueil et les deux pages relatives aux données personnelles. Les ancres
  internes ne sont pas des pages distinctes ; aucune date de modification
  artificielle n’est publiée.
- Le workflow [SEO checks](.github/workflows/seo-checks.yml) contrôle la cohérence
  entre domaine, métadonnées, images, données structurées et fichiers d’exploration.

Contrôle local sans dépendance :

```sh
python3 scripts/check-seo.py
```

Lors d’un changement de domaine, mettre à jour ensemble `CNAME`, la page HTML,
`robots.txt` et `sitemap.xml`. Conserver les descriptions conformes aux modes
réellement présentés, sans annoncer Strava ou le coaching comme disponibles.

Limites : ces fichiers préparent l’indexation ; ils ne garantissent ni classement
ni résultat enrichi. Aucun prix, avis ou score n’est inventé dans le JSON-LD.
La publication dépend de la fusion et de GitHub Pages. Le contrôle local ne
valide pas le DNS, les redirections HTTPS ou l’indexation effective.

Après publication, vérifier les réponses HTTP de la page, de `robots.txt` et du
sitemap, puis soumettre `https://rouleur.club/sitemap.xml` et inspecter l’URL dans
Google Search Console avec un compte autorisé. Ces opérations restent à effectuer.
Voir les références Google sur les
[URL canoniques](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls)
et les [sitemaps](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).


## Confidentialité et suppression des données

Les pages statiques publiques sont accessibles sans connexion :

- [Politique de confidentialité](confidentialite/index.html) → `https://rouleur.club/confidentialite/`
- [Instructions de suppression](suppression-des-donnees/index.html) → `https://rouleur.club/suppression-des-donnees/`

Elles partagent [assets/legal.css](assets/legal.css), sont liées dans le pied de
page et dans le sitemap. Elles ne chargent ni script ni police externe. Le responsable indiqué est **Codio** ; le contact public est
**benjamin@codio.be**, conformément aux coordonnées fournies par le propriétaire
du projet. Les marqueurs `A_CONFIRMER` bloquent le contrôle SEO normal et ne
doivent pas être publiés. L’option `--allow-draft` est réservée à la rédaction
locale ; la CI utilise toujours le contrôle normal.

### Périmètre et références de rédaction

Le contenu décrit le code de Rouleur au commit `9a0085f` :

- [Authentification](https://github.com/bevrard/legend/blob/9a0085f/src/app/services/legend-auth.service.ts),
  [profil et bibliothèque](https://github.com/bevrard/legend/blob/9a0085f/src/app/services/legend-cloud-user.service.ts),
  [progression des séances](https://github.com/bevrard/legend/blob/9a0085f/src/app/services/legend-session-tracking.service.ts).
- [Demandes de support](https://github.com/bevrard/legend/blob/9a0085f/src/app/services/feedback.service.ts)
  et [transfert vers GitHub](https://github.com/bevrard/legend/blob/9a0085f/scripts/sync-feedback-to-github.mjs).
- [Stockage local GPX](https://github.com/bevrard/legend/blob/9a0085f/src/app/pages/echappee/session.models.ts),
  [analyse/génération](https://github.com/bevrard/legend/blob/9a0085f/functions/index.mjs),
  [accès et limites réseau](https://github.com/bevrard/legend/blob/9a0085f/functions/inventory-access.mjs),
  [prestataires](https://github.com/bevrard/legend/blob/9a0085f/docs/integrations/overview.md)
  et [rétention des sauvegardes](https://github.com/bevrard/legend/blob/9a0085f/docs/ci-cd/firestore-backups.md).
- [Information des personnes — CNIL](https://www.cnil.fr/fr/conformite-rgpd-information-des-personnes-et-transparence)
  et [droit à l’effacement — APD](https://www.dataprotectionauthority.be/professionnel/rgpd-/droits-des-citoyens/droit-a-l-effacement).

Aucun bouton de suppression de compte ni traitement automatique des demandes
n’est ajouté par ces pages. La procédure publiée doit être assurée manuellement
par le responsable : vérifier le compte, supprimer l’identité d’authentification
et les données associées (y compris sous-collections, séances, préparations et
copies de support), puis confirmer le résultat. Retirer l’application de Facebook
ou supprimer le seul utilisateur Firebase Auth ne supprime pas tout Firestore.
Les données locales restent à effacer sur chaque appareil. Les sauvegardes suivent
leur cycle de conservation ; les exceptions légales doivent être motivées.

L’expiration d’une analyse de parcours après une heure ne prouve pas un effacement
physique automatique. Les durées techniques, les garanties de transfert et les
services réellement utilisés doivent être revus avec leur configuration lorsque
l’application évolue. Cette documentation ne certifie ni une acceptation Meta ni
la conformité de tous les parcours de l’application.

Après fusion et déploiement GitHub Pages, vérifier les deux URLs publiques avant
de les renseigner dans Meta. La vérification d’entreprise/identité Meta reste une
opération séparée.
