/*
 * PWN05 - User Management
 * Category: Binary & Exploitation (C) - Use-After-Free / Function Pointer Hijack
 * Difficulty: Medium
 *
 * Story: A tiny HR "user management" console. It lets you create a
 * user, delete them, view their profile, and add a free-text "note"
 * about them. The bug: deleting a user frees its struct but never
 * clears the dangling `current_user` pointer, and viewing a profile
 * blindly calls a function pointer stored inside that struct.
 *
 * This is deliberately built as a CONTROLLED UAF rather than relying
 * on the allocator's undefined behavior after free():
 *   - struct User and struct Note are exactly the same size, so a
 *     Note allocated right after a User is freed reliably reclaims
 *     that same chunk on glibc's tcache (single-threaded, small,
 *     same-size-class object).
 *   - The Note's fields are laid out to deliberately alias the
 *     User's fields: a name buffer at the same offset, and a
 *     function-pointer-sized field at the same offset as
 *     print_profile. The player fully controls that memory via the
 *     "add note" input.
 *   - No dependency on heap metadata corruption, no double-free,
 *     no need to defeat tcache safe-linking - just: free, reclaim
 *     with attacker data, then trigger the stale pointer.
 *
 * Intended solution:
 *   1) create a user
 *   2) delete the user (frees the chunk; current_user still points at it)
 *   3) add a note whose raw bytes overlay print_profile with the
 *      address of win() (leaked via the binary being non-PIE, or via
 *      the menu's built-in "debug: leak win() address" option for a
 *      beginner-friendly version - see LEAK_WIN_ADDR below)
 *   4) view profile -> calls the hijacked pointer -> win() runs and
 *      prints the flag
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Set to 1 for the beginner-friendly variant of this challenge that
// exposes win()'s address through the menu (teaches the UAF/hijack
// concept without also requiring an infoleak). Set to 0 to make
// players find/derive the address themselves (e.g. via `objdump`,
// since the binary is compiled non-PIE for this challenge).
#define LEAK_WIN_ADDR 1

#define NAME_LEN 24

struct User {
    char name[NAME_LEN];
    void (*print_profile)(struct User *);
};

struct Note {
    char text[NAME_LEN];
    unsigned long fake_fn_ptr; // aliases User.print_profile when reclaimed
};

static struct User *current_user = NULL;

void default_print_profile(struct User *u) {
    printf("Profile: %s\n", u->name);
}

void win(struct User *u) {
    (void)u;
    printf("\n[!] Function pointer hijacked -> win() reached!\n");
    FILE *f = fopen("flag.txt", "r");
    if (!f) {
        printf("[!] flag.txt not found on this host.\n");
        return;
    }
    char buf[256];
    if (fgets(buf, sizeof(buf), f)) {
        printf("%s", buf);
    }
    fclose(f);
}

void create_user(void) {
    if (current_user) {
        printf("A user already exists. Delete them first.\n");
        return;
    }
    current_user = malloc(sizeof(struct User));
    memset(current_user, 0, sizeof(struct User));

    printf("Enter name: ");
    char buf[256];
    if (!fgets(buf, sizeof(buf), stdin)) return;
    buf[strcspn(buf, "\n")] = 0;
    strncpy(current_user->name, buf, NAME_LEN - 1);

    current_user->print_profile = default_print_profile;
    printf("User created.\n");
}

void delete_user(void) {
    if (!current_user) {
        printf("No user to delete.\n");
        return;
    }
    free(current_user);
    // BUG: current_user is never set back to NULL, leaving a
    // dangling pointer that later menu options still use.
    printf("User deleted.\n");
}

void view_profile(void) {
    if (!current_user) {
        printf("No user loaded.\n");
        return;
    }
    // BUG: calls through a function pointer stored in memory that
    // may have been freed and reallocated as something else.
    current_user->print_profile(current_user);
}

void add_note(void) {
    // Same allocation size as struct User, so on a fresh single
    // -threaded tcache it reliably reuses the just-freed User chunk.
    struct Note *n = malloc(sizeof(struct Note));
    memset(n, 0, sizeof(struct Note));

    printf("Enter note text (max %d chars): ", NAME_LEN - 1);
    char buf[256];
    if (!fgets(buf, sizeof(buf), stdin)) return;
    buf[strcspn(buf, "\n")] = 0;
    strncpy(n->text, buf, NAME_LEN - 1);

    printf("Enter fake function pointer value (decimal, 0 to skip): ");
    char numbuf[64];
    if (fgets(numbuf, sizeof(numbuf), stdin)) {
        unsigned long val = strtoul(numbuf, NULL, 0);
        if (val != 0) {
            n->fake_fn_ptr = val;
        }
    }

    printf("Note stored at %p.\n", (void *)n);
    // Deliberately "leaked": the note is not freed here, mirroring a
    // real app that keeps notes around. This is what lets the note's
    // bytes persist in the reclaimed chunk for the later UAF call.
}

void menu(void) {
    printf("\n==== USER MANAGEMENT ====\n");
    printf("1) Create user\n");
    printf("2) Delete user\n");
    printf("3) View profile\n");
    printf("4) Add note\n");
#if LEAK_WIN_ADDR
    printf("5) [debug] leak win() address\n");
#endif
    printf("6) Exit\n");
    printf("> ");
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    printf("=== HR USER MANAGEMENT CONSOLE ===\n");

    char choice[16];
    while (1) {
        menu();
        if (!fgets(choice, sizeof(choice), stdin)) break;

        switch (atoi(choice)) {
            case 1: create_user(); break;
            case 2: delete_user(); break;
            case 3: view_profile(); break;
            case 4: add_note(); break;
#if LEAK_WIN_ADDR
            case 5:
                printf("win() is at %p\n", (void *)win);
                break;
#endif
            case 6:
                printf("Goodbye.\n");
                return 0;
            default:
                printf("Invalid option.\n");
        }
    }
    return 0;
}
