# Accueil et applications

## Tigris et Arc

Sur le second Stick, [Tigris](https://github.com/lesnolie/Tigris) **2.0.16 Standard** a été installé depuis la publication officielle et son SHA256 comparé au fichier de sommes du projet. Package `com.leslie.tvhome`, accueil `.HomeActivity`. Navigation physique confirmée par l'utilisateur.

Le système était déjà `fr-FR`, mais cette version de Tigris n'avait que les ressources anglais/chinois. Passer Android en français ne traduit pas ses menus. Aucune version modifiée de Tigris n'a été créée.

Sur cette ROM, `set-home-activity` seul laissait l'accueil Google prioritaire. La configuration finale a nécessité de désactiver le launcher Google **pour l'utilisateur0**, sans le désinstaller :

```sh
adb -s SERIAL shell pm disable-user --user 0 com.google.android.tvlauncher
adb -s SERIAL shell cmd package set-home-activity com.leslie.tvhome/.HomeActivity
adb -s SERIAL shell input keyevent 3
```

Ne faire cette opération qu'après avoir installé et vérifié le nouvel accueil. Retour Google :

```sh
adb -s SERIAL shell pm enable --user 0 com.google.android.tvlauncher
adb -s SERIAL shell cmd package set-home-activity com.google.android.tvlauncher/.MainActivity
adb -s SERIAL shell input keyevent 3
```

Arc1.1.0 ARMv7 avait également été testé sur le premier Stick. Ne pas installer de variantes ARM64 sur ce système32bits.

## Applications installées sur le second appareil

| Application | Version installée |
| --- | --- |
| Prime Video Android TV | 6.24.13+v16.0.1.93-allAbis, splits ARMv7/français/xhdpi |
| Disney+ Android TV | 26.20.0+rc1-2026.10.22, variante Android12L+ ARMv7, splits français/xhdpi |
| Amazon Music Android TV | 3.4.1294.0 ARMv7 nodpi |
| Netflix | Déjà présent, conservé |

Le Play Store indiquait une incompatibilité pour Prime Video/Disney+ et une indisponibilité territoriale pour Music. Des APK Android TV signés par leurs éditeurs ont été installés directement depuis APKMirror, avec contrôle de signature via `apksigner`. Les écrans de lancement s'affichent ; cela **ne certifie pas le DRM ni la lecture des contenus**.

Préférer le Play Store lorsque disponible. Pour une installation manuelle : contrôler package, varianteTV, ABI, SDKminimal et certificat. Une archive `.apkm` est un ensemble de splits : installer le base et les splits requis pour le matériel/langue/densité avec `adb install-multiple`, pas la seule archive renommée en APK. Ne pas supprimer une application existante pour contourner une divergence de signature.

## Marqueur de build et VOO TV+

Sur le premier appareil, la version observée de VOO TV+ refusait le marqueur `Build.TAGS` contenant `test-keys`. Modifier sous TWRP l'unique ligne `ro.build.tags=test-keys` de `build.prop` en `ro.build.tags=custom`, tout en préservant ses attributs, a permis d'atteindre l'écran de connexion. Le même ajustement a été appliqué sur le second Stick.

Ce changement n'est **ni une suppression générale du root, ni une certification Play Integrity/Widevine, ni une garantie de lecture**. Il n'est pas nécessaire au correctif Bluetooth. Ne pas déclarer arbitrairement une ROM officielle ou remplacer les APK des services pour masquer leur origine.
