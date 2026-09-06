#!/usr/bin/env bash
# Сборка мода без Gradle: компиляция против библиотек, уже скачанных PrismLauncher.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PRISM="${PRISM:-$HOME/.local/share/PrismLauncher}"
LIB="$PRISM/libraries"
JAVA_HOME_21="${JAVA_HOME_21:-$PRISM/java/java-runtime-delta}"
JAVAC="$JAVA_HOME_21/bin/javac"
JAR="$JAVA_HOME_21/bin/jar"
NEO_VER="${NEO_VER:-21.1.248}"
MC_ART="${MC_ART:-1.21.1-20240808.144430}"
MODS="${MODS:-$PRISM/instances/1.21.1/minecraft/mods}"

CP="$LIB/net/neoforged/neoforge/$NEO_VER/neoforge-$NEO_VER-client.jar"
CP="$CP:$LIB/net/neoforged/neoforge/$NEO_VER/neoforge-$NEO_VER-universal.jar"
CP="$CP:$LIB/net/minecraft/client/$MC_ART/client-$MC_ART-srg.jar"
CP="$CP:$LIB/net/minecraft/client/$MC_ART/client-$MC_ART-extra.jar"
while IFS= read -r j; do CP="$CP:$j"; done < <(
  find "$LIB" -name '*.jar' \
    ! -path '*/com/mojang/minecraft/*' \
    ! -path '*/net/minecraft/client/*' \
    ! -path '*/net/neoforged/neoforge/*' \
    ! -name '*-installer.jar' | sort)
JEI="$(ls "$MODS"/jei-*.jar 2>/dev/null | head -1 || true)"
[ -n "$JEI" ] && CP="$CP:$JEI"

OUT="$ROOT/build/classes"
rm -rf "$OUT" "$ROOT/build/libs"
mkdir -p "$OUT" "$ROOT/build/libs"

find "$ROOT/src/main/java" -name '*.java' > "$ROOT/build/sources.txt"
"$JAVAC" -nowarn -proc:none -encoding UTF-8 --release 21 \
  -cp "$CP" -d "$OUT" "@$ROOT/build/sources.txt"

cp -r "$ROOT/src/main/resources/." "$OUT/"
mkdir -p "$OUT/data/codex"
cp -r "$OUT/assets/codex/book" "$OUT/data/codex/book"
"$JAR" --create --file "$ROOT/build/libs/codex-aeternum-1.0.0.jar" -C "$OUT" .
echo "Готово: $ROOT/build/libs/codex-aeternum-1.0.0.jar"
