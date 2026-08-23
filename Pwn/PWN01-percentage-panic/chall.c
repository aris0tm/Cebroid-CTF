/*
 * PWN01 - Percentage Panic
 * Category: Binary Exploitation (C) - Stack Overflow
 * Difficulty: Easy
 *
 * Story: A frantic exam-grading terminal that computes your percentage
 * score. It never checks how long your name is before copying it into
 * a fixed-size buffer.
 *
 * Intended solution: overwrite the adjacent `is_admin` flag (or the
 * saved return address, depending on how you want to teach it) by
 * supplying a name longer than the buffer.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void print_flag(void) {
    FILE *f = fopen("flag.txt", "r");
    if (!f) {
        printf("[!] flag.txt not found on this host. Ask an admin.\n");
        return;
    }
    char buf[256];
    if (fgets(buf, sizeof(buf), f)) {
        printf("%s", buf);
    }
    fclose(f);
}

void calculate_percentage(void) {
    char name[32];
    int is_admin = 0;         // <-- sits right after `name` on the stack
    int marks, total;
    char input[512];

    printf("Enter your name: ");
    fflush(stdout);

    // gets() was removed from modern glibc, so we reimplement an
    // equally unsafe pattern: read a large line, then strcpy it into
    // the small fixed buffer with NO bounds check.
    if (!fgets(input, sizeof(input), stdin)) {
        return;
    }
    input[strcspn(input, "\n")] = 0;   // strip trailing newline
    strcpy(name, input);               // deliberately unsafe: no bounds checking

    printf("Enter marks obtained: ");
    scanf("%d", &marks);
    printf("Enter total marks: ");
    scanf("%d", &total);

    if (total == 0) {
        printf("Total marks can't be zero, nice try.\n");
        return;
    }

    float pct = (marks / (float)total) * 100.0f;
    printf("\nHello, %s!\n", name);
    printf("Your percentage: %.2f%%\n", pct);

    if (is_admin) {
        printf("\n[!] Admin override detected!\n");
        print_flag();
    } else {
        printf("(Regular student access only.)\n");
    }
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    printf("=== PERCENTAGE PANIC ===\n");
    printf("The end-of-term grading terminal is melting down.\n\n");
    calculate_percentage();
    return 0;
}
