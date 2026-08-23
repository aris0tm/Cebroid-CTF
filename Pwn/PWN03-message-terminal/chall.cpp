/*
 * PWN03 - Message Terminal
 * Category: Binary & Exploitation (C++) - Format String
 * Difficulty: Easy
 *
 * Story: A chat/message terminal that echoes whatever you type. It
 * passes your input directly as the format string instead of as data.
 *
 * Vulnerable line:
 *     printf(msg.c_str());
 * instead of the safe:
 *     printf("%s", msg.c_str());
 *
 * The secret flag is loaded into a local variable and sits on the
 * stack near the format-string call, so %x / %p / %s leaks can pull
 * it out without ever needing the source.
 */

#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>

std::string load_flag() {
    std::ifstream f("flag.txt");
    std::string flag = "CYBROID{flag_file_missing}";
    if (f.good()) {
        std::getline(f, flag);
    }
    return flag;
}

void message_terminal() {
    // The flag is loaded into a stack-local std::string buffer here,
    // so its bytes are reachable via stack-walking %x/%p leaks, and
    // its C-string data is reachable via a %s leak if you find the
    // right offset / pointer on the stack.
    std::string flag = load_flag();
    volatile const char *flag_ptr = flag.c_str(); // keep it alive & addressable
    (void)flag_ptr;

    std::cout << "=== MESSAGE TERMINAL ===\n";
    std::cout << "Type a message and it will be echoed back.\n";
    std::cout << "> ";

    std::string msg;
    std::getline(std::cin, msg);

    printf("Echo: ");
    printf(msg.c_str());   // <-- the bug: user input used as format string
    printf("\n");
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    message_terminal();
    return 0;
}
