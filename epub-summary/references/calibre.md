# Calibre en secours

Vérifier dans WSL : `command -v ebook-convert`, puis `ebook-convert --version`.

Le chemin TXT active la sortie Markdown :

```bash
ebook-convert '/chemin/livre.epub' '/cache/nouveau-dossier/livre.txt' --txt-output-formatting markdown --keep-links
```

Consulter `ebook-convert input.epub output.txt --help` pour les options de la version installée. `--formatting-type` décrit l'entrée TXT ; ce n'est pas le sélecteur de sortie Markdown. Garder le suffixe `.txt` pour choisir le plugin TXT. Ne pas écraser une extraction existante.

La conversion peut modifier les titres, liens et frontières. Comparer son résultat au sommaire et au spine original, conserver la commande/version et inventorier toutes les lacunes. Ne pas réutiliser les IDs d'une autre extraction ; attribuer des plages de lignes propres à ce résultat. Lire les chapitres retenus en entier. Une sortie convertie seule ne prouve pas que le livre a été intégralement extrait. Normaliser U+2014 dans les textes dérivés en signalant cette transformation ; vérifier toute citation dans l'original.

Si le livre est chiffré ou essentiellement constitué d'images, signaler la limite et demander une source accessible. Pas de contournement de DRM, pas d'OCR silencieux, pas de prise en charge implicite des autres formats.

Documentation officielle : https://manual.calibre-ebook.com/generated/en/ebook-convert.html
Structure EPUB : https://www.w3.org/TR/epub-33/
