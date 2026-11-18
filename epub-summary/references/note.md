# Modèle de note

Le modèle et le YAML du vault priment. Pour pro-vault, reprendre Date, Catégorie, Related Day, Auteur, URL et tags du modèle Livres ; conserver les clés existantes, ajouter `Source` avec l'URL connue ou, sans URL, l'URI locale explicite du livre. Ne pas inventer une URL commerciale. Enregistrer aussi `source_sha256`, `extraction_version` et `analysis_status`. Les nouvelles clés générales sont en anglais. Le titre et l'auteur proviennent de l'EPUB, avec les incertitudes signalées.

Structure à adapter au genre et au volume :

```markdown
# Titre du livre

## Présentation
Auteur, édition/langue si connues, type de livre, sujet ou cadre narratif et ambition. Pour un roman : avertissement sur les révélations.

## Synthèse générale
Proposition centrale ou trajectoire narrative, progression du livre et conclusion. Relier les chapitres dans leur ordre, sans transformer le livre en catalogue de thèmes.

## Lecture par chapitre
### Titre réel du chapitre
Résumé, arguments ou événements, exemples et nuances qui changent la compréhension. Repères précis vers les passages.

## Points essentiels à retenir
Enseignements transversaux sourcés. Distinguer application personnelle, interprétation et propos de l'auteur.

## Concepts, nuances et questions
Concepts reliés par wikilinks, limites et tensions, pistes à approfondir. Pour un roman, motifs, style et ambiguïtés.

## Sources et couverture
Livre et empreinte ; repères de chapitre, chemin XHTML, ancre ou bloc d'extraction. Chemin du cache et du manifeste. Chapitres/segments traités, exclusions motivées, problèmes d'extraction et contenus visuels non analysés.
```

Un repère lisible contient le contexte, par exemple : « Chapitre Mémoire, section Consolidation, EPUB `Text/ch04.xhtml#sleep`, extraction `spine-0005 / section-0012 / b000143` ». Ne pas citer un identifiant seul. Les références d'extraction sont stables seulement pour l'empreinte et la version indiquées. Le cache reste local : un lien local ne devient pas une source consultable sur les autres appareils. Conserver assez de contexte XHTML dans la note pour vérifier dans le livre original.

La note publiée n'embarque pas le texte intégral ni toutes les analyses techniques. Les citations restent brèves et vérifiées. Les chapitres exclus et la qualité d'extraction font partie de la note, même si le cache existe ailleurs.
