// the file is written in c and use cpp compiler because the obfuscate only supports cpp.

#include <grp.h>
#include <pwd.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

#include "obfuscate.h"

#define REPORT(msg) exit(printf(msg))

enum fperm {
    FPERM_X = 1 << 0,
    FPERM_W = 1 << 1,
    FPERM_R = 1 << 2,
};

struct fmode {
    uint8_t usr;
    uint8_t grp;
    uint8_t oth;
};

struct fmode fmode(const uint32_t st_mode) {
    struct fmode fm;
    fm.usr = (st_mode >> 6) & 07;
    fm.grp = (st_mode >> 3) & 07;
    fm.oth = st_mode & 07;
    return fm;
}

int main() {
    struct stat     st;
    struct fmode    fm;
    int             stat_ret;
    struct group*   grp;
    struct passwd*  pwd;
    bool            rk_mem;
    bool            usr_mem;
    FILE*           fp;
    const char*     flag;

    stat_ret = stat("flag.txt", &st);
    if (stat_ret != 0) REPORT("create a file named 'flag.txt' and i (ricky) will write the flag into it for you (challenger)!\n创建一个名为 'flag.txt' 的文件, 我 (ricky) 将会为你 (challenger) 把 flag 写入到这个文件里.\n");

    fm  = fmode(st.st_mode);
    grp = getgrgid(st.st_gid);
    pwd = getpwuid(st.st_uid);

    if (strcmp(grp->gr_name, "rknazo"))     REPORT("add new group named 'rknazo' and set the file's group to 'rknazo'.\n创建组 'rknazo' 并将文件的组设置为 'rknazo'.\n");
    if (strcmp(pwd->pw_name, "challenger")) REPORT("add new user named 'challenger' and set the file's user to 'challenger'.\n创建用户 'challenger' 并将文件的用户设置为 'challenger'.\n");

    rk_mem  = false;
    usr_mem = false;

    for (size_t i = 0; grp->gr_mem[i] != NULL; i++) {
        if (!rk_mem && strcmp(grp->gr_mem[i], "ricky")) rk_mem = true;
        if (!usr_mem && strcmp(grp->gr_mem[i], "challenger")) usr_mem = true;
        if (rk_mem && usr_mem) break;
    }

    if (!rk_mem || !usr_mem) REPORT("add new user named 'ricky' and add it and 'challenger' to group 'rknazo'.\n创建用户 'ricky' 并将其和 'challenger' 添加到组 'rknazo'.\n");

    if (fm.oth)                 REPORT("i don't want anyone else except you and me could access the flag.\n我不想让除了你和我之外的人能访问 flag.\n");
    if (!(fm.usr & FPERM_R))    REPORT("you must have read access to this file.\n你必须要有这个文件的读取权限.\n");
    if (fm.usr & FPERM_W)       REPORT("i don't hope you could write the file.\n我不希望你能写入这个文件.\n");
    if (fm.usr & FPERM_X || fm.grp & FPERM_X)
                                REPORT("this file should not be executable.\n这个文件不需要执行权限.\n");
    if (fm.grp & FPERM_R)       REPORT("i don't need to read the file for i can write to it without any doubt, believe me!\n我不需要读取权限, 我闭着眼都能写对的, 相信我!\n");
    if (!(fm.grp & FPERM_W))    REPORT("oops, i can't write to the file!\n诶呀, 我没法写入这个文件啊!\n");

    flag    = "flag{}";
    fp      = fopen("flag.txt", "w");

    fprintf(fp, "%s\n", flag);
    fclose(fp);

    REPORT("cheers! you passed the challenge!\n恭喜你, 通过了挑战!\n");
}
