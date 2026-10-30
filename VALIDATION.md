# Vérification et retour arrière

## Fin de configuration

- `sys.boot_completed=1`.
- `device_provisioned=1` et `user_setup_complete=1`.
- Accueil accessible, réseau et navigation fonctionnels.

## Reconnexion Bluetooth

- Association AR conservée sans suppression manuelle de la base.
- Bluetooth ON et absence de nouveaux crashes.
- HID connecté : `mInputDevices` contient l'appareil avec l'état2.
- Trois redémarrages logiciels successifs.
- Après reboot, appui bref sur une flèche/centre ; aucun maintien Accueil, reset ou nouvel appairage.
- Confirmation physique des boutons après le premier et le dernier redémarrage.

Ces critères ont été remplis sur les deux appareils testés. Ne pas interpréter un état HID0 au repos comme un échec avant d'avoir réveillé normalement la télécommande. À l'inverse, une association enregistrée seule ne prouve pas une connexion utilisable.

Les essais avant la fin de l'assistant ne sont pas comptés : SetupWraith avait supprimé une association lors d'un timeout de validation.

## Accueil et raccourcis

- Vérifier le composant HOME résolu, le retour par Accueil et la navigation.
- Après reboot, vérifier le service de raccourcis lié et non crashé.
- Appuyer physiquement sur les quatre touches ; les événements injectés ADB ne reproduisent pas nécessairement leur parcours complet.
- Pour Music, attendre cinq secondes et vérifier l'absence de second lancement de Netflix.

## Sauvegardes et mises à jour

Conserver hors dépôt : images des partitions critiques, originaux de bibliothèque/keylayout/build.prop, empreintes, manifestes du patch et clé de signature du service. Les rapports Android/HCI et bases Bluetooth peuvent contenir des identifiants et clés : ne pas les publier.

Une mise à jour de ROM peut remplacer le binaire Bluetooth, le keylayout et le marqueur de build. **Ne jamais réappliquer les offsets à un hash différent.** Refaire l'analyse et la validation.

Retours arrière ciblés :

- BibliothèqueBluetooth : original exact-build sous TWRP, attributs et hash contrôlés ; garder les associations.
- Boutons : keylayout original + désactivation/désinstallation du service local.
- Accueil : réactiver le launcher Google et rétablir HOME.
- Marqueur de build : fichier original avec ses attributs.

Un retour complet Fire OS est une opération distincte dépendant des images et de la chaîne de démarrage. Ce guide ne promet pas qu'un simple flash de la sauvegarde boot suffit à restaurer l'appareil.
