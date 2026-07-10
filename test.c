#include <stdio.h>
#include <string.h>

void erase_password(char *password) {
    volatile char *vpass = password;
    while (*vpass) {
        *vpass++ = '\0';
    }
}
int main() {
    char p[] = "hello";
    erase_password(p);
    return 0;
}
