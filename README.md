# Jennis Coiffure — site web

Salon de coiffure dame à Abidjan (Côte d’Ivoire) · WhatsApp +225 07 88 71 15 92

Site vitrine statique en français (HTML + CSS + JavaScript, sans dépendance), généré à partir du modèle « firm-portfolio-site ».

## Structure

- `site.json` — **tout le contenu du site** (nom, slogan, couleurs, équipe, prestations et tarifs, réalisations, actualités, adresse, horaires, contact).
- `images/` — logo et photos du salon (découpées depuis les visuels fournis).
- `generator/` — le générateur (`build.py`) et les fichiers CSS/JS.
- `docs/` — le site généré, prêt à être publié.

## Modifier le site

1. Modifiez `site.json` (textes, prix, adresse, e-mail…). Pour les images, indiquez un chemin (ex. `images/balayage.jpg`) ou une URL ; sans image, une illustration provisoire est générée.
2. Régénérez le site :
   ```bash
   python3 generator/build.py site.json docs
   ```
3. Prévisualisez : `python3 -m http.server -d docs` puis ouvrez http://localhost:8000.

## Pages

Accueil · Le salon (Recrutement) · Réalisations (tressage, tissage, natté, coiffure, homme & enfant) · Prestations (coiffure, coiffure homme & enfant, soins capillaires, manucure & pédicure, produits de beauté) · Actualités · Contact

Pour ajouter une page « L’équipe », remplissez la liste `team` dans `site.json` (nom, rôle, photo).

## Formulaire de contact

Le formulaire ouvre WhatsApp avec un message pré-rempli (nom, téléphone, prestation, message) vers le numéro `contact.whatsapp`. Un bouton WhatsApp flottant est présent sur toutes les pages.

## Publication (GitHub Pages)

Paramètres du dépôt → Pages → Branche principale, dossier `/docs`.
