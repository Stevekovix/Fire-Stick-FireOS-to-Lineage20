# Migration testée

## 1. Identifier l'appareil et autoriser ADB

Activer les options développeur et le débogage ADB dans Fire OS. Brancher un câble de données USB et accepter l'autorisation du PC sur la TV.

```sh
adb devices -l
adb -s SERIAL shell getprop ro.product.device
adb -s SERIAL shell getprop ro.product.model
adb -s SERIAL shell getprop ro.build.display.id
adb -s SERIAL shell getprop ro.build.version.incremental
```

Les essais concernent `sheldonp`, AFTSSS, PS7717.5741N / 0036408028548. **Ne pas déduire la compatibilité d'un autre firmware à partir de cette liste.** Suivre les profils et restrictions du mainteneur GhostLock.

## 2. Root temporaire et sauvegardes

Récupérer GhostLock depuis son projet d'origine. Contrôler le profil exact avant exécution. Sur la configuration testée, le profil intégré était `sheldon-PS7717.5741`, matériel testé par le projet, chemin `configfs-mm-reclaim-v1`. Le Wi-Fi avait été désactivé avant l'exploitation.

Une fois le root temporaire obtenu, sauvegarder **avant toute écriture** :

- `lk`, `tee1`, `tee2`, `boot`, `recovery` ;
- les régions eMMC `mmcblk0boot0` et `mmcblk0boot1` ;
- la GPT primaire et les propriétés système.

Sur ce matériel, les partitions nommées étaient accessibles sous `/dev/block/platform/soc/11230000.mmc/by-name/`. Copier les sauvegardes vers le PC et vérifier leurs SHA256. Ne jamais publier ces dumps ou les réutiliser comme identité d'un autre Stick.

## 3. Préchargeur, Kamakiri et TWRP

La chaîne suivie était : root temporaire GhostLock → downgrade du préchargeur compatible → Kamakiri natif sous Linux → fastboot modifié → TWRP.

Le préchargeur utilisé pour le downgrade GhostLock avait une taille de **157696 octets**, SHA256 :

```text
40c64e2df52c969c766f9dc39e044dac9241bf4c6cda66e860a2aa0ce2c30d34
```

Il est **différent** du préchargeur livré dans notre répertoire Kamakiri. Ce dépôt ne le redistribue pas et ne fournit pas de commande générique pour écrire boot0 : la procédure amont et les contrôles de cible restent nécessaires. L'écriture réalisée a été suivie d'une relecture et d'une comparaison de hash, avec reprotection de `force_ro`.

Sur Linux, arrêter ModemManager si nécessaire avant la capture du port préchargeur. Lancer `bootrom-step.sh` depuis la distribution Kamakiri correcte, puis redémarrer le Stick ; le redémarrage ADB a suffi lors de nos essais. Attendre la fin effective des étapes RPMB/TZ/LK/payload/microloader avant de poursuivre. Ne pas ignorer un avertissement de modèle ou de GPT.

Une fois fastboot disponible et la cible vérifiée :

```sh
fastboot -s SERIAL flash recovery CHEMIN_VERS_TWRP_COMPATIBLE.img
fastboot -s SERIAL oem reboot-recovery
```

Ces commandes supposent un bootloader déjà préparé par la chaîne compatible, pas un Fire OS standard verrouillé.

## 4. Installer les archives

Empreintes des fichiers utilisés :

| Archive | SHA256 |
| --- | --- |
| LineageOS20 20260923 | `e8f3f97d6888c242dc012f58ed015fa3c546a43a5d005949aa00a0f01615a7e2` |
| TZ PS7669 | `3d11513b14d3163efb31c8dda5d07d111a5f7b605cdfdf13ca79d21bdf4c8179` |
| MindTheGapps13 ARM ATV minimal 20240311 | `126e9b8ba33793e84cd32ee983b3e8eb7d8a24afea89836abc7719e14272d9b8` |

Comparer les archives téléchargées et les copies sur le Stick. Les hashes ci-dessus identifient nos fichiers, sans remplacer la vérification de provenance.

Sous TWRP, après sauvegarde et en acceptant la perte des données Fire OS : nettoyer data/cache puis installer, **dans cet ordre** :

1. TZ PS7669.
2. LineageOS20.
3. MindTheGapps ARM ATV minimal, **avant le premier démarrage Android**.

Contrôler le code de retour de chaque installation et les patches amonet dans `recovery.log`. Lors des essais, `twrp wipe data` conservait `/data/media` : ce n'était pas un effacement sécurisé intégral. Le client CLI pouvait rester bloqué après la fin réelle du nettoyage ; vérifier le journal avant de relancer quoi que ce soit. La TV et son HDMI doivent être opérationnels, TWRP pouvant attendre l'affichage.

## 5. Correctifs et premier démarrage

Le correctif Bluetooth a été appliqué sous TWRP, selon [BLUETOOTH.md](BLUETOOTH.md). Sur le second appareil neuf, un PRAND propre à cet appareil a été fixé **avant la première association**. Ne pas copier la bibliothèque patchée, l'IRK ou la base Bluetooth d'un autre Stick.

Configurer langue, réseau et comptes directement sur la TV. Une première association est nécessaire. Si la télécommande refuse le mode appairage, suivre la procédure Amazon adaptée au modèle ; le bouton Power peut fonctionner en infrarouge sans Bluetooth.

**Terminer l'assistant jusqu'à l'accueil.** Dans notre incident, SetupWraith a exécuté `onPrepairedAwaitSelectTimedout: timed out and removing bond` après 30 secondes d'attente du bouton central. La disparition de l'association provenait alors de l'assistant, pas d'un défaut de persistance Bluetooth. Vérifier :

```sh
adb -s SERIAL shell settings get global device_provisioned
adb -s SERIAL shell settings get secure user_setup_complete
```

Les deux valeurs doivent être `1` avant de commencer les tests de reconnexion.
