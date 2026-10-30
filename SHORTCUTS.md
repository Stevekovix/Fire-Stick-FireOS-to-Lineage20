# Boutons Netflix, Prime Video, Disney+ et Amazon Music

## Configuration matérielle observée

La télécommande AR utilisait `/vendor/usr/keylayout/Vendor_0171_Product_0421.kl` (identifiants `0171:0421`). Les appuis physiques, effectués dans un ordre connu, ont donné :

| Bouton | Scancode Linux | Code Android initial | Application |
| --- | --- | --- | --- |
| Netflix | 744 / `0x2e8` | BUTTON_1 / 188 | `com.netflix.ninja` |
| Prime Video | 745 / `0x2e9` | BUTTON_2 / 189 | `com.amazon.amazonvideo.livingroom` |
| Disney+ | 746 / `0x2ea` | BUTTON_3 / 190 | `com.disney.disneyplus` |
| Amazon Music | 747 / `0x2eb` | BUTTON_4 / 191 | `com.amazon.music.tv` |

Ces correspondances doivent être **mesurées sur votre télécommande**, pas supposées à partir de la disposition des logos. `getevent -pl`, puis `getevent -lt /dev/input/eventN` ont servi à relever les événements. Le numéro eventN peut changer.

## Service de raccourcis

Source : `ShortcutService.java`, avec `AndroidManifest.xml` et `accessibility-shortcuts.xml`. Ce service d'accessibilité intercepte seulement les codes dédiés et lance l'activité Android TV du paquet correspondant. Il ne demande pas Internet, n'accède pas au contenu des fenêtres et n'enregistre pas les frappes.

Pour Prime Video, une première implémentation via `resolveActivity()` ne trouvait pas l'activité LEANBACK sans catégorie DEFAULT, et affichait à tort « application non installée ». La version corrigée utilise `queryIntentActivities(intent, 0)`, puis une activité explicite ; un lancement standard sert de secours.

Compiler avec JDK, SDK Android API33+, `d8`, `aapt`, `apksigner` et `zip`. Indiquer les chemins via les variables demandées par `build-shortcuts.sh`. Créer et conserver votre propre clé de signature en local ; ne pas l'ajouter au dépôt. Aucun SDK ou APK compilé n'est redistribué ici.

```sh
adb -s SERIAL install --no-incremental out/tv-shortcuts.apk
```

Activer **Raccourcis télécommande** dans Paramètres → Accessibilité. L'activation d'un service d'accessibilité peut entraîner une confirmation Android ; vérifier qu'il s'agit bien du service compilé depuis ces sources. Ne pas écraser la liste des autres services activés par une commande `settings put` générique.

## Conflit spécifique Amazon Music → Netflix

Sur notre ROM, Music était lancé correctement par le service, mais le système (`uid1000`) lançait immédiatement Netflix à son tour pour le même bouton. Un délai de relance aurait seulement masqué le conflit.

Le correctif appliqué sous TWRP modifie **une seule ligne** du keylayout AR actif :

```diff
-key 747   BUTTON_4    WAKE
+key 747   F12         WAKE
```

F12 vaut Android142 ; le service inclut cette correspondance vers Music. Le traitement natif du code191 ne se déclenche donc plus pour ce bouton.

Avant édition : sauvegarder le keylayout, vérifier la cible matérielle et la ligne originale. Sous notre TWRP, la partition vendor `mmcblk0p10` était montée sur `/vendor`. Préserver propriétaire0:0, mode0644 et contexte `u:object_r:vendor_keylayout_file:s0`, relire le fichier, puis redémarrer.

Les trois autres touches, les touches de navigation et les réglages Bluetooth ne sont pas modifiés par ce changement. Une mise à jour ROM peut réécrire vendor.

## Validation et retrait

Après reboot : vérifier le service lié dans `dumpsys accessibility`, puis appuyer sur chaque bouton physique. Attendre au moins cinq secondes sur Music pour vérifier que Netflix ne prend pas sa place.

L'utilisateur a confirmé Prime Video et, après le changement F12 et un reboot, Amazon Music restant affiché. Les lancements Netflix/Disney ont également été enregistrés par le service.

Pour revenir en arrière : restaurer le keylayout sauvegardé sous TWRP, désactiver uniquement ce service dans Accessibilité puis désinstaller `local.androidtv.shortcuts`. Ne pas effacer les associations Bluetooth pour retirer les raccourcis.
