#include <stdio.h>
#include <string.h>

const char flag[] = "flag{}";


int main() {
    char buf[50];
    printf("please type your flag (请输入 flag):\n");
    fgets(buf, sizeof(buf), stdin);
    buf[strcspn(buf, "\r\n")] = 0;  // remove newline char
    if (strcmp(flag, buf) == 0) {
        printf("cheers! you've got the flag!\n");
        printf("恭喜! 你拿到了 flag!\n");
    } else {
        printf("oh no, that's not correct!\n");
        printf("呜呜呜, 那个 flag 不对!\n");
    }
}
