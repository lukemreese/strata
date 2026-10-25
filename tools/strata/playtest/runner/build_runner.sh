#!/bin/bash
# Builds tools/strata/playtest/runner/strata-runner: mGBA 0.10.5's GBA core plus
# strata_runner.c, with no cmake, Qt, SDL or Lua needed (only gcc, zlib, libpng).
# The mGBA source is cloned once into $MGBA_SRC (default ~/.cache/mgba-0.10.5).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
MGBA_SRC="${MGBA_SRC:-$HOME/.cache/mgba-0.10.5}"
OUT="$HERE/build"
if [ ! -f "$MGBA_SRC/src/gba/core.c" ]; then
  mkdir -p "$(dirname "$MGBA_SRC")"
  git clone --depth 1 --branch 0.10.5 https://github.com/mgba-emu/mgba.git "$MGBA_SRC"
fi
mkdir -p "$OUT/include/mgba" "$OUT/obj"
cat > "$OUT/include/mgba/flags.h" <<'EOF'
#ifndef FLAGS_H
#define FLAGS_H
#define M_CORE_GBA
#define USE_PNG
#define USE_ZLIB
#define USE_PTHREADS
#define HAVE_CRC32
#define HAVE_LOCALTIME_R
#define HAVE_STRDUP
#define HAVE_STRNDUP
#endif
EOF
cat > "$OUT/version.c" <<'EOF'
#include <mgba/core/version.h>
MGBA_EXPORT const char* const gitCommit = "0.10.5";
MGBA_EXPORT const char* const gitCommitShort = "0.10.5";
MGBA_EXPORT const char* const gitBranch = "0.10.5";
MGBA_EXPORT const int gitRevision = 0;
MGBA_EXPORT const char* const binaryName = "strata-runner";
MGBA_EXPORT const char* const projectName = "mGBA";
MGBA_EXPORT const char* const projectVersion = "0.10.5";
EOF
S="$MGBA_SRC/src"
SRCS=(
  arm/arm.c arm/decoder-arm.c arm/decoder.c arm/decoder-thumb.c arm/isa-arm.c arm/isa-thumb.c
  core/bitmap-cache.c core/cache-set.c core/cheats.c core/config.c core/core.c core/directories.c
  core/input.c core/interface.c core/library.c core/lockstep.c core/log.c core/map-cache.c
  core/mem-search.c core/rewind.c core/serialize.c core/sync.c core/thread.c core/tile-cache.c core/timing.c
  gb/audio.c
  gba/audio.c gba/bios.c gba/cart/ereader.c gba/cart/gpio.c gba/cart/matrix.c gba/cart/vfame.c
  gba/cheats.c gba/cheats/codebreaker.c gba/cheats/gameshark.c gba/cheats/parv3.c gba/core.c gba/dma.c
  gba/gba.c gba/hle-bios.c gba/input.c gba/io.c gba/memory.c gba/overrides.c gba/renderers/cache-set.c
  gba/renderers/common.c gba/renderers/software-bg.c gba/renderers/software-mode0.c
  gba/renderers/software-obj.c gba/renderers/video-software.c gba/savedata.c gba/serialize.c
  gba/sharkport.c gba/sio.c gba/sio/gbp.c gba/sio/joybus.c gba/timer.c gba/video.c
  gba/extra/audio-mixer.c gba/extra/proxy.c gba/extra/battlechip.c
  util/circle-buffer.c util/configuration.c util/crc32.c util/formatting.c util/gbk-table.c util/hash.c
  util/string.c util/table.c util/vfs.c util/convolve.c util/elf-read.c util/export.c util/patch.c
  util/patch-fast.c util/patch-ips.c util/patch-ups.c util/png-io.c util/ring-fifo.c util/text-codec.c
  util/vfs/vfs-fd.c util/vfs/vfs-dirent.c util/vfs/vfs-mem.c
  feature/video-logger.c feature/thread-proxy.c util/vfs/vfs-fifo.c platform/posix/memory.c third-party/inih/ini.c third-party/blip_buf/blip_buf.c
)
CFLAGS=(-O2 -std=gnu11 -w -fno-strict-aliasing -I"$OUT/include" -I"$MGBA_SRC/include" -I"$MGBA_SRC/src"
  -I"$S/third-party/inih" -I"$S/third-party/blip_buf" -DBUILD_STATIC -D_GNU_SOURCE -DHAVE_STRTOF_L
  -DHAVE_NEWLOCALE -DHAVE_FREELOCALE -DHAVE_USELOCALE -DHAVE_SETLOCALE -DHAVE_CHMOD -DHAVE_UMASK
  -DHAVE_LOCALE -DMGBA_STANDALONE -DM_CORE_GBA -DUSE_PNG -DUSE_ZLIB -DUSE_PTHREADS -DHAVE_CRC32
  -DHAVE_LOCALTIME_R -DHAVE_STRDUP -DHAVE_STRNDUP)
# Rebuild everything when the flags change.
STAMP="$(echo "${CFLAGS[*]}" | md5sum | cut -c1-12)"
if [ "$(cat "$OUT/obj/.flags" 2>/dev/null)" != "$STAMP" ]; then rm -f "$OUT"/obj/*.o; echo "$STAMP" > "$OUT/obj/.flags"; fi
OBJS=()
pids=()
for f in "${SRCS[@]}" ; do
  o="$OUT/obj/$(echo "$f" | tr '/' '_' | sed 's/\.c$/.o/')"
  OBJS+=("$o")
  if [ ! -f "$o" ] || [ "$S/$f" -nt "$o" ]; then
    gcc "${CFLAGS[@]}" -c "$S/$f" -o "$o" &
    pids+=($!)
    if [ ${#pids[@]} -ge 8 ]; then wait "${pids[0]}"; pids=("${pids[@]:1}"); fi
  fi
done
for p in "${pids[@]}"; do wait "$p"; done
gcc "${CFLAGS[@]}" -c "$OUT/version.c" -o "$OUT/obj/version.o"
gcc "${CFLAGS[@]}" -Wall -c "$HERE/strata_runner.c" -o "$OUT/obj/strata_runner.o"
gcc -o "$HERE/strata-runner" "$OUT/obj/strata_runner.o" "$OUT/obj/version.o" "${OBJS[@]}" -lpng -lz -lpthread -lm
echo "built $HERE/strata-runner"
