# Reconnexion de la télécommande Amazon AR

## Observation et limite du diagnostic

Avant correction, l'association pouvait rester enregistrée après reboot, mais les tentatives LE échouaient avec `0x3e` avant les échanges GATT/HID et le chiffrement. Sur le premier appareil, les échecs analysés survenaient autour de 264 ms. Ce code n'est pas à confondre avec le timeout de supervision `0x08`.

Le scan à 60 ms, une tentative d'adresse publique, les boucles de connexion et un appel Java HID n'ont pas résolu le problème observé. Il ne faut pas inventer des propriétés `persist.bluetooth.*` ni utiliser `bluetoothctl` comme si Android utilisait BlueZ.

Le contournement validé maintient le **PRAND du Stick stable** entre redémarrages. Cela ne prouve pas une cause universelle du défaut du microprogramme Amazon ; les essais établissent le résultat sur nos appareils.

## Principe

Dans `LeAddressManager::generate_rpa()`, remplacer les deux chargements du PRAND aléatoire par deux instructions `movw` constantes. La fonction conserve son calcul AES avec **l'IRK propre à l'appareil**. Aucun partage de clé entre appareils n'est nécessaire.

L'adresse privée d'initiation reste ainsi constante lorsque l'IRK est inchangée. **La rotation de cette adresse destinée à limiter le suivi Bluetooth est réduite.** Le chiffrement n'est pas désactivé, et les clés d'association ne sont pas supprimées.

## Bibliothèque exacte prise en charge

- ARM32 / Thumb-2, pas AArch64.
- SHA256 original : `50a44a7dfa32e5cea2a46135c8460981609bef99164e0f9bfb3f0ffc23504f3c`.
- Taille observée : 10026516 octets.
- Fichier Android : `/system/apex/com.android.btservices/lib/libbluetooth_jni.so`.
- Sous notre TWRP : `/system_root/system/apex/com.android.btservices/lib/libbluetooth_jni.so`.
- Adresses virtuelles : `0x64b562` et `0x64b566`.
- Offset fichier : `0x64a562`, longueur 8 octets.
- Octets attendus : `9df81600bdf81410`.

**Ne pas reporter ces offsets sur une autre version. Ne pas faire de remplacement global de constantes, ni écrire une valeur 16 bits au milieu d'une instruction Thumb.**

## Préparer la copie

Installer radare2 et Python3. Le script ne télécharge rien, ne se connecte pas au Stick et ne flashe rien.

Pour un appareil neuf, **avant la première association** :

```sh
python3 prepare_stable_rpa.py private/libbluetooth_jni.original.so out/libbluetooth_jni.stable-rpa.so --new-device
```

Pour conserver une association déjà fonctionnelle, capturer la **RPA locale du Stick**, puis utiliser son PRAND actuel :

- Une adresse locale affichée `AB:CD:EF:12:34:56` contient le PRAND dans ses trois premiers octets affichés.
- L'argument `--prand-le` est dans l'ordre inversé de ces trois octets. Utiliser les valeurs **réellement capturées**, jamais l'exemple.
- Les deux bits de poids fort doivent être `01`. Ne pas confondre adresse du contrôleur, adresse de la télécommande et RPA locale.

```sh
python3 prepare_stable_rpa.py private/libbluetooth_jni.original.so out/libbluetooth_jni.stable-rpa.so --prand-le HEX_REEL_DE_3_OCTETS
```

Le script refuse les builds inattendues, les sorties existantes, les modifications hors zone et un encodage MOVW divergent. Il écrit un manifeste local avec hash d'entrée/sortie et PRAND. **Une sortie préparée n'est pas une validation sur appareil.**

## Installation sous TWRP

1. Sauvegarder la bibliothèque originale sur le PC.
2. Monter la partition système correcte en lecture/écriture ; dans notre GPT, `mmcblk0p11` monté sur `/system_root`.
3. Revérifier le hash original sur le Stick et le hash de la copie transférée.
4. Remplacer le contenu du fichier existant en préservant propriétaire `0:0`, mode `0644` et contexte `u:object_r:system_lib_file:s0`.
5. Relire le hash final et vérifier les attributs avant de redémarrer.

Ne pas remplacer une bibliothèque système à chaud. Ne pas copier `bt_config.conf`, l'IRK ou les sauvegardes d'un autre Stick. Une mise à jour ROM peut écraser la bibliothèque ; toute nouvelle build nécessite une nouvelle analyse.

## Vérifier et revenir en arrière

Faire trois redémarrages logiciels après la fin de l'assistant. Réveiller normalement la télécommande par une flèche ou le bouton central, sans maintien Accueil. Dans `dumpsys bluetooth_manager`, vérifier association et état HID `2`, puis vérifier les boutons physiquement.

Une trace HCI peut confirmer `LE Set Random Address` identique, connexion suivie de trafic ACL et chiffrement avec réutilisation du lien. Les rapports complets peuvent contenir des clés et identifiants : les garder privés. Désactiver la capture complète après diagnostic, les propriétés persistantes survivant au reboot.

Pour annuler : restaurer **la bibliothèque originale de cet appareil et de cette build** sous TWRP, préserver ses attributs, contrôler le hash, redémarrer. Ne pas effacer les associations pour restaurer le binaire.
