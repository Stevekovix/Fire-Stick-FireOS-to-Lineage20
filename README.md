# Fire Stick (FireOS) to Lineage20

J'ai installé LineageOS 20 sur deux Fire TV Stick pour pouvoir utiliser Android TV et installer des applications plus récentes que celles disponibles sur mon ancien Fire OS.

L'installation de la ROM n'a pas été le plus long. Le vrai problème, c'était la télécommande : elle fonctionnait après l'association, puis ne répondait plus après un redémarrage. Ensuite, certains boutons lançaient la mauvaise application — Amazon Music ouvrait Netflix.

Ce dépôt rassemble la procédure suivie et les corrections qui ont fonctionné sur mes appareils. L'idée est d'éviter à d'autres de refaire les mêmes essais, tout en précisant ce qui a vraiment été testé.

## Avant de commencer

Mes appareils sont des **Fire TV Stick AFTSSS / `sheldonp`, ARM 32 bits**. Ils utilisaient Fire OS **PS7717.5741N**, incrémental **0036408028548**.

Ce guide ne s'applique pas automatiquement aux autres Fire Stick, même s'ils se ressemblent. Il faut vérifier le modèle, le firmware et les prérequis des outils utilisés. Le déverrouillage et l'installation effacent des données ; une mauvaise image peut empêcher le Stick de démarrer. Les sauvegardes sont donc à faire avant toute modification.

## Ce qui fonctionne chez moi

- LineageOS 20 / Android TV 13 démarre avec les services Google.
- La télécommande Amazon AR permet de naviguer et se reconnecte après redémarrage.
- Trois redémarrages logiciels successifs ont été validés sur chaque appareil après correction.
- Tigris est installé sur le second Stick pour avoir un accueil plus proche d'Apple TV.
- Netflix est conservé ; Prime Video, Disney+ et Amazon Music sont installés.
- Les boutons dédiés ouvrent les applications prévues, avec une correction supplémentaire pour Amazon Music.

Je n'ai pas validé la lecture de tous les services, le DRM, la HD/4K ni le comportement après une coupure électrique prolongée. Je préfère le préciser plutôt que d'annoncer une compatibilité « 100 % » que je n'ai pas vérifiée.

## Par où commencer ?

| Ce que vous cherchez | Guide |
| --- | --- |
| Passer de Fire OS à LineageOS 20 | [Installation](MIGRATION.md) |
| Corriger la reconnexion de la télécommande | [Bluetooth](BLUETOOTH.md) |
| Régler Netflix, Prime Video, Disney+ et Amazon Music | [Boutons et raccourcis](SHORTCUTS.md) |
| Changer l'accueil et installer les applications | [Accueil et applications](LAUNCHERS_APPS.md) |
| Vérifier le résultat et revenir en arrière | [Tests et restauration](VALIDATION.md) |

**Un piège à éviter : terminez l'assistant Android TV avant de tester les redémarrages.** Dans mon cas, cet assistant supprimait lui-même l'association lorsqu'il attendait trop longtemps la validation du bouton central. Cela ressemblait à un problème Bluetooth, alors que la connexion avait réussi.

## Versions utilisées

- TWRP **3.6.1_9-0**, avec la chaîne GhostLock / Kamakiri adaptée au matériel.
- `sheldon-tz-PS7669.zip`.
- `lineage-20.0-20260923-UNOFFICIAL-sheldon.zip`.
- `MindTheGapps-13.0.0-arm-ATV-minimal-20240311_051455.zip`.

Les empreintes des archives et les contrôles à effectuer sont dans le guide d'installation. Le correctif Bluetooth est volontairement limité au hash de la bibliothèque analysée : il refuse une autre version.

## Ce que je partage

La documentation, les sources du service de raccourcis et le script qui prépare une copie patchée de la bibliothèque Bluetooth. Le script ne flashe rien tout seul.

Les sauvegardes des Sticks, les clés, les journaux privés, les firmwares et les APK des éditeurs ne sont pas inclus. Chaque appareil garde sa propre identité Bluetooth. Pour compiler les raccourcis, utilisez votre propre clé de signature et gardez-la hors du dépôt.

## Merci aux projets à l'origine de cette installation

- [GhostLock](https://github.com/R0rt1z2/GhostLock/tree/4.4)
- [Kamakiri et TWRP pour sheldon/sheldonp](https://xdaforums.com/t/unlock-root-twrp-unbrick-fire-tv-stick-3-and-fire-tv-stick-lite-sheldon-p.4410297/)
- [LineageOS 20 pour sheldon](https://github.com/amazon-oss/releases/releases/tag/lineage-20-sheldon-v0.5)
- [MindTheGapps ARM ATV](https://github.com/MindTheGapps/13.0.0-arm-ATV/releases)
- [Tigris](https://github.com/lesnolie/Tigris)
- [Arc Launcher](https://github.com/meddouribadis/arclauncher), essayé sur le premier Stick

Ce dépôt est mon retour d'expérience. Il n'est pas une publication officielle de ces projets et ne remplace pas leurs consignes de compatibilité.
