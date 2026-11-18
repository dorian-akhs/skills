# Modèle de note

Le format et la destination viennent de la conversation et du contexte du harness. Dans un vault, son modèle, ses métadonnées et ses instructions priment. Hors vault, utiliser le format convenu sans imposer de YAML ni de wikilinks. Si la destination ou le format restent ambigus, demander à l'utilisateur avant la rédaction finale.

Conserver le titre, l'auteur, la source et les incertitudes éventuelles. Fournir l'URL connue ou, sans URL, une référence locale explicite au livre ; ne pas inventer une URL commerciale. Garder l'empreinte source, la version d'extraction et le statut d'analyse dans le format approprié, dans la note ou son rapport de couverture, sans imposer de noms de propriétés propres à un vault.

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
Concepts, limites et tensions, pistes à approfondir. Liens adaptés au format et au contexte. Pour un roman, motifs, style et ambiguïtés.

## Sources et couverture
Livre et empreinte ; repères de chapitre, chemin XHTML, ancre ou bloc d'extraction. Chemin du cache et du manifeste. Chapitres/segments traités, exclusions motivées, problèmes d'extraction et contenus visuels non analysés.
```

Un repère lisible contient le contexte, par exemple : « Chapitre Mémoire, section Consolidation, EPUB `Text/ch04.xhtml#sleep`, extraction `spine-0005 / section-0012 / b000143` ». Ne pas citer un identifiant seul. Les références d'extraction sont stables seulement pour l'empreinte et la version indiquées. Le cache reste local : un lien local ne devient pas une source consultable sur les autres appareils. Conserver assez de contexte XHTML dans la note pour vérifier dans le livre original.

La note publiée n'embarque pas le texte intégral ni toutes les analyses techniques. Les citations restent brèves et vérifiées. Les chapitres exclus et la qualité d'extraction font partie de la note, même si le cache existe ailleurs.
