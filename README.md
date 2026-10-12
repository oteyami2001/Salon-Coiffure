# Salon Coiffure — site web

Site vitrine statique en français (HTML + CSS + JavaScript, sans dépendance), généré à partir du modèle « firm-portfolio-site ».

## Structure

- `site.json` — **tout le contenu du site** (nom, slogan, couleurs, équipe, prestations et tarifs, réalisations, actualités, adresse, horaires, contact).
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

Accueil · Le salon (L’équipe, Recrutement) · Réalisations (femme, homme, couleur, événements) · Prestations (coupe & brushing, coloration, soins, barbier) · Actualités · Contact

## Formulaire de contact

Par défaut le formulaire ouvre la messagerie (`mailto:`). Pour recevoir les messages directement, renseignez `contact.form_action` avec une adresse Formspree (ou équivalent).

## Publication (GitHub Pages)

Paramètres du dépôt → Pages → Branche principale, dossier `/docs`.
