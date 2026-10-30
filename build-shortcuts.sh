#!/bin/sh
set -eu
cd "$(dirname "$0")"
: "ANDROID_JAR:?Chemin vers android.jar API33 ou plus récent"
: "D8:?Chemin vers d8 du SDK Android"
: "AAPT:?Chemin vers aapt du SDK Android"
: "APKSIGNER:?Chemin vers apksigner du SDK Android"
: "KEYSTORE:?Votre keystore de signature local (ne pas publier)"
: "KEY_ALIAS:?Alias dans votre keystore"
mkdir -p out/classes out/dex out/res/xml
cp accessibility-shortcuts.xml out/res/xml/shortcuts.xml
javac -source 8 -target 8 -classpath "$ANDROID_JAR" -d out/classes ShortcutService.java
"$D8" --min-api 28 --output out/dex out/classes/local/androidtv/shortcuts/ShortcutService.class
"$AAPT" package -f -M AndroidManifest.xml -S out/res -I "$ANDROID_JAR" -F out/unsigned.apk
(cd out/dex && zip -q ../unsigned.apk classes.dex)
# apksigner demande le mot de passe interactivement ; aucun secret codé en dur.
"$APKSIGNER" sign --ks "$KEYSTORE" --ks-key-alias "$KEY_ALIAS" --out out/tv-shortcuts.apk out/unsigned.apk
"$APKSIGNER" verify out/tv-shortcuts.apk
