// ae-hpd.c
// Minimal Hyprland wallpaper daemon

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dirent.h>
#include <signal.h>
#include <time.h>
#include <sys/stat.h>
#include <sys/types.h>

#define CONFIG_FILE "ae-hpd.conf"
#define MAX_WALLPAPERS 1024
#define MAX_PATH 512

static volatile sig_atomic_t reload_config_flag = 0;

typedef struct {
    int interval;               // seconds
    char wallpapers[MAX_WALLPAPERS][MAX_PATH];
    int count;
} Config;

Config config;

void handle_sighup(int sig) {
    reload_config_flag = 1;
}

// Load config file
int load_config(const char *file) {
    FILE *f = fopen(file, "r");
    if (!f) {
        perror("Failed to open config file");
        return 0;
    }

    char line[MAX_PATH];
    config.count = 0;
    config.interval = 60; // default 60s

    while (fgets(line, sizeof(line), f)) {
        if (line[0] == '#' || line[0] == '\n') continue;

        // Interval line: interval=30
        if (strncmp(line, "interval=", 9) == 0) {
            config.interval = atoi(line + 9);
        }
        // Wallpaper paths
        else {
            line[strcspn(line, "\n")] = 0; // strip newline
            if (config.count < MAX_WALLPAPERS) {
                strncpy(config.wallpapers[config.count], line, MAX_PATH);
                config.count++;
            }
        }
    }

    fclose(f);
    return 1;
}

// Pick next wallpaper in rotation
int current_index = 0;
const char* next_wallpaper() {
    if (config.count == 0) return NULL;
    const char *path = config.wallpapers[current_index];
    current_index = (current_index + 1) % config.count;
    return path;
}

// Set wallpaper using hyprctl
void set_wallpaper(const char *path) {
    char cmd[MAX_PATH + 32];
    snprintf(cmd, sizeof(cmd), "hyprctl hyprpaper set \"%s\"", path);
    system(cmd);
}

int main() {
    // Daemonize
    if (fork() != 0) return 0;
    setsid();
    signal(SIGHUP, handle_sighup);

    if (!load_config(CONFIG_FILE)) return 1;

    while (1) {
        if (reload_config_flag) {
            printf("Reloading config...\n");
            load_config(CONFIG_FILE);
            reload_config_flag = 0;
        }

        const char *wall = next_wallpaper();
        if (wall) set_wallpaper(wall);

        sleep(config.interval);
    }

    return 0;
}
