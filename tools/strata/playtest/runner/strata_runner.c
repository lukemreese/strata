/* strata-runner: a headless mGBA (0.10.5 core) driven over stdin/stdout.
 *
 * Built by tools/strata/playtest/build_runner.sh. The Python harness
 * (tools/strata/playtest/harness.py) starts it and speaks this protocol; each
 * command is one line, each reply is one line starting with "ok" or "err".
 *
 *   step N KEYS [ADDR LEN]  hold KEYS (hex GBA key mask) for N frames, then reply
 *                           "ok FRAME [HEX]" with LEN bytes read at ADDR
 *   r8|r16|r32 ADDR         read (no side effects)          -> "ok VALUE" (hex)
 *   rd ADDR LEN             read LEN bytes                  -> "ok HEX"
 *   w8|w16|w32 ADDR VALUE   write
 *   wd ADDR HEX             write bytes
 *   shot PATH               write the last frame as PNG
 *   hash                    CRC32 of the last frame         -> "ok CRC"
 *   ss PATH | ls PATH       save / load a state file
 *   sav PATH                write the cartridge save (SRAM/flash) to PATH
 *   regs                    -> "ok r0 .. r15 cpsr" (hex)
 *   stats                   -> "ok frame=N resets=N errors=N"
 *   log                     -> "ok [json strings]" and clears the log buffer
 *   reset                   hard reset
 *   quit
 *
 * Options: strata-runner ROM [--sav FILE] [--rtc UNIX_SECONDS]
 * The save is loaded into memory only: the file is never written.
 * Resets: SWI 0x00 (SoftReset) is counted. Crashes: mGBA's "Jumped to invalid
 * address" and other GAME_ERROR lines are recorded with the PC.
 */
#include <mgba/core/core.h>
#include <mgba/core/log.h>
#include <mgba/core/serialize.h>
#include <mgba/internal/arm/arm.h>
#include <mgba/internal/gba/gba.h>
#include <mgba-util/png-io.h>
#include <mgba-util/vfs.h>

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <zlib.h>

#define W 240
#define H 160
#define LOG_MAX 400

static struct mCore* core;
static color_t* video;
static unsigned resets;
static unsigned errors;
static char* logLines[LOG_MAX];
static unsigned logRepeat[LOG_MAX];
static unsigned logCount;
static void (*origSwi16)(struct ARMCore*, int);
static void (*origSwi32)(struct ARMCore*, int);

static unsigned pc(void) {
	struct GBA* gba = core->board;
	return (unsigned) gba->cpu->gprs[15];
}

static void addLog(const char* line) {
	if (logCount && strcmp(logLines[logCount - 1], line) == 0) {
		logRepeat[logCount - 1]++;
		return;
	}
	if (logCount == LOG_MAX) {
		free(logLines[0]);
		memmove(logLines, logLines + 1, sizeof(logLines[0]) * (LOG_MAX - 1));
		memmove(logRepeat, logRepeat + 1, sizeof(logRepeat[0]) * (LOG_MAX - 1));
		logCount--;
	}
	logLines[logCount] = strdup(line);
	logRepeat[logCount] = 1;
	logCount++;
}

static void logger(struct mLogger* l, int category, enum mLogLevel level, const char* format, va_list args) {
	(void) l;
	const char* cat = mLogCategoryName(category);
	bool gameDebug = cat && strcmp(cat, "GBA Debug") == 0;
	if (!(level & (mLOG_FATAL | mLOG_ERROR | mLOG_GAME_ERROR)) && !(gameDebug && (level & (mLOG_INFO | mLOG_WARN | mLOG_DEBUG)))) {
		return;
	}
	if (!gameDebug && (level & (mLOG_FATAL | mLOG_ERROR | mLOG_GAME_ERROR))) {
		errors++;
	}
	char msg[512];
	vsnprintf(msg, sizeof(msg), format, args);
	char line[700];
	snprintf(line, sizeof(line), "%s|%s|pc=%08X|%s", gameDebug ? "game" : "error", cat ? cat : "?", core ? pc() : 0, msg);
	addLog(line);
}

static struct mLogger sLogger = { .log = logger, .filter = NULL };

static void swi16(struct ARMCore* cpu, int imm) {
	if (imm == 0x00) {
		resets++;
		char line[64];
		snprintf(line, sizeof(line), "reset|SoftReset|pc=%08X|", (unsigned) cpu->gprs[15]);
		addLog(line);
	}
	origSwi16(cpu, imm);
}

static void swi32(struct ARMCore* cpu, int imm) {
	if ((imm >> 16) == 0x00) {
		resets++;
		addLog("reset|SoftReset|arm|");
	}
	origSwi32(cpu, imm);
}

static void hexOut(uint32_t addr, uint32_t len) {
	static const char digits[] = "0123456789abcdef";
	for (uint32_t i = 0; i < len; i++) {
		unsigned b = core->rawRead8(core, addr + i, -1);
		putchar(digits[b >> 4]);
		putchar(digits[b & 15]);
	}
}

static void jsonString(const char* s) {
	putchar('"');
	for (; *s; s++) {
		unsigned char c = *s;
		if (c == '"' || c == '\\') {
			putchar('\\');
			putchar(c);
		} else if (c < 0x20) {
			printf("\\u%04x", c);
		} else {
			putchar(c);
		}
	}
	putchar('"');
}

static bool writePng(const char* path) {
	struct VFile* vf = VFileOpen(path, O_CREAT | O_TRUNC | O_WRONLY);
	if (!vf) {
		return false;
	}
	png_structp png = PNGWriteOpen(vf);
	png_infop info = PNGWriteHeader(png, W, H);
	bool ok = PNGWritePixels(png, W, H, W, video);
	PNGWriteClose(png, info);
	vf->close(vf);
	return ok;
}

static void runFrames(unsigned n, uint32_t keys) {
	core->setKeys(core, keys);
	for (unsigned i = 0; i < n; i++) {
		core->runFrame(core);
	}
}

int main(int argc, char** argv) {
	if (argc < 2) {
		fprintf(stderr, "usage: %s ROM [--sav FILE] [--rtc UNIX_SECONDS]\n", argv[0]);
		return 2;
	}
	const char* rom = argv[1];
	const char* sav = NULL;
	long long rtc = -1;
	for (int i = 2; i + 1 < argc; i += 2) {
		if (strcmp(argv[i], "--sav") == 0) {
			sav = argv[i + 1];
		} else if (strcmp(argv[i], "--rtc") == 0) {
			rtc = atoll(argv[i + 1]);
		}
	}
	mLogSetDefaultLogger(&sLogger);
	core = mCoreFind(rom);
	if (!core || !core->init(core)) {
		fprintf(stderr, "cannot create a core for %s\n", rom);
		return 1;
	}
	mCoreInitConfig(core, NULL);
	mCoreConfigSetDefaultValue(&core->config, "idleOptimization", "detect");
	core->opts.mute = true;
	core->opts.skipBios = true;
	mCoreLoadConfig(core);
	video = calloc(W * H, sizeof(color_t));
	core->setVideoBuffer(core, video, W);
	core->setAudioBufferSize(core, 2048);
	if (!mCoreLoadFile(core, rom)) {
		fprintf(stderr, "cannot load %s\n", rom);
		return 1;
	}
	/* The save lives in memory: never touch the file. */
	struct VFile* save = NULL;
	if (sav) {
		struct VFile* in = VFileOpen(sav, O_RDONLY);
		if (in) {
			ssize_t size = in->size(in);
			void* buf = malloc(size);
			in->seek(in, 0, SEEK_SET);
			in->read(in, buf, size);
			in->close(in);
			save = VFileMemChunk(buf, size);
			free(buf);
		}
	}
	if (!save) {
		save = VFileMemChunk(NULL, 0);
	}
	core->loadSave(core, save);
	if (rtc >= 0) {
		core->rtc.override = RTC_FIXED;
		core->rtc.value = rtc * 1000LL;
	}
	core->reset(core);
	struct GBA* gba = core->board;
	gba->hardCrash = false;
	origSwi16 = gba->cpu->irqh.swi16;
	origSwi32 = gba->cpu->irqh.swi32;
	gba->cpu->irqh.swi16 = swi16;
	gba->cpu->irqh.swi32 = swi32;

	setvbuf(stdout, NULL, _IOFBF, 1 << 16);
	char line[1 << 16];
	while (fgets(line, sizeof(line), stdin)) {
		char cmd[16] = {0};
		char arg[4096] = {0};
		unsigned long a = 0, b = 0, c = 0, d = 0;
		int n = sscanf(line, "%15s", cmd);
		if (n < 1) {
			continue;
		}
		const char* rest = line + strlen(cmd);
		while (*rest == ' ') {
			rest++;
		}
		if (strcmp(cmd, "step") == 0) {
			int k = sscanf(rest, "%lu %lx %lx %lu", &a, &b, &c, &d);
			if (k < 2) {
				puts("err step N KEYS [ADDR LEN]");
			} else {
				runFrames(a, b);
				printf("ok %u", core->frameCounter(core));
				if (k == 4) {
					putchar(' ');
					hexOut(c, d);
				}
				putchar('\n');
			}
		} else if (strcmp(cmd, "r8") == 0 || strcmp(cmd, "r16") == 0 || strcmp(cmd, "r32") == 0) {
			sscanf(rest, "%lx", &a);
			uint32_t v = cmd[1] == '8' ? core->rawRead8(core, a, -1) : cmd[1] == '1' ? core->rawRead16(core, a, -1) : core->rawRead32(core, a, -1);
			printf("ok %x\n", v);
		} else if (strcmp(cmd, "rd") == 0) {
			sscanf(rest, "%lx %lu", &a, &b);
			printf("ok ");
			hexOut(a, b);
			putchar('\n');
		} else if (strcmp(cmd, "w8") == 0 || strcmp(cmd, "w16") == 0 || strcmp(cmd, "w32") == 0) {
			sscanf(rest, "%lx %lx", &a, &b);
			if (cmd[1] == '8') {
				core->rawWrite8(core, a, -1, b);
			} else if (cmd[1] == '1') {
				core->rawWrite16(core, a, -1, b);
			} else {
				core->rawWrite32(core, a, -1, b);
			}
			puts("ok");
		} else if (strcmp(cmd, "wd") == 0) {
			char* hex = malloc(strlen(rest) + 1);
			sscanf(rest, "%lx %s", &a, hex);
			size_t len = strlen(hex) / 2;
			for (size_t i = 0; i < len; i++) {
				unsigned v;
				sscanf(hex + i * 2, "%2x", &v);
				core->rawWrite8(core, a + i, -1, v);
			}
			free(hex);
			puts("ok");
		} else if (strcmp(cmd, "shot") == 0) {
			sscanf(rest, "%4095[^\n]", arg);
			puts(writePng(arg) ? "ok" : "err cannot write png");
		} else if (strcmp(cmd, "hash") == 0) {
			printf("ok %08lx\n", crc32(0, (const Bytef*) video, W * H * sizeof(color_t)));
		} else if (strcmp(cmd, "ss") == 0 || strcmp(cmd, "ls") == 0) {
			sscanf(rest, "%4095[^\n]", arg);
			bool saveIt = cmd[0] == 's';
			struct VFile* vf = VFileOpen(arg, saveIt ? O_CREAT | O_TRUNC | O_RDWR : O_RDONLY);
			bool ok = vf && (saveIt ? mCoreSaveStateNamed(core, vf, SAVESTATE_SAVEDATA | SAVESTATE_RTC)
			                        : mCoreLoadStateNamed(core, vf, SAVESTATE_SAVEDATA | SAVESTATE_RTC));
			if (vf) {
				vf->close(vf);
			}
			puts(ok ? "ok" : "err state");
		} else if (strcmp(cmd, "sav") == 0) {
			sscanf(rest, "%4095[^\n]", arg);
			void* data = NULL;
			size_t size = core->savedataClone(core, &data);
			FILE* f = fopen(arg, "wb");
			if (f) {
				fwrite(data, 1, size, f);
				fclose(f);
			}
			free(data);
			puts(f ? "ok" : "err cannot write save");
		} else if (strcmp(cmd, "regs") == 0) {
			printf("ok");
			for (int i = 0; i < 16; i++) {
				printf(" %08x", (unsigned) gba->cpu->gprs[i]);
			}
			printf(" %08x\n", (unsigned) gba->cpu->cpsr.packed);
		} else if (strcmp(cmd, "stats") == 0) {
			printf("ok frame=%u resets=%u errors=%u\n", core->frameCounter(core), resets, errors);
		} else if (strcmp(cmd, "log") == 0) {
			printf("ok [");
			for (unsigned i = 0; i < logCount; i++) {
				char buf[760];
				if (logRepeat[i] > 1) {
					snprintf(buf, sizeof(buf), "%s (x%u)", logLines[i], logRepeat[i]);
				} else {
					snprintf(buf, sizeof(buf), "%s", logLines[i]);
				}
				if (i) {
					putchar(',');
				}
				jsonString(buf);
				free(logLines[i]);
			}
			logCount = 0;
			puts("]");
		} else if (strcmp(cmd, "reset") == 0) {
			core->reset(core);
			puts("ok");
		} else if (strcmp(cmd, "quit") == 0) {
			puts("ok");
			break;
		} else {
			printf("err unknown command %s\n", cmd);
		}
		fflush(stdout);
	}
	fflush(stdout);
	core->deinit(core);
	return 0;
}
