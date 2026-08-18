#!/usr/bin/env bash
# Compile the Android app and surface Gradle/Kotlin failures as check annotations.
set -o pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG="${RUNNER_TEMP:-/tmp}/atlas-android-build.log"

cd "$ROOT/android" || exit 1
if ./gradlew :app:testDebugUnitTest :app:assembleDebug --stacktrace 2>&1 | tee "$LOG"; then
  exit 0
fi

# GitHub's external log storage is not always reachable from every client. Emit
# concise compiler diagnostics through the Checks annotations API as well.
mapfile -t diagnostics < <(grep -E '(^e: |error: |FAILURE:|What went wrong:|Execution failed for task|Could not determine|SDK location)' "$LOG" | tail -n 30)
if [ "${#diagnostics[@]}" -eq 0 ]; then
  diagnostics=("Android build failed; inspect the Gradle output in this step.")
fi
for line in "${diagnostics[@]}"; do
  line="${line//'%'/'%25'}"
  line="${line//$'\r'/'%0D'}"
  line="${line//$'\n'/'%0A'}"
  echo "::error title=Android build::$line"
done
exit 1
