# perm

本题考验 Unix 权限及 busybox 权限设置命令。

## 解题过程

下面每一步都需执行 `./challenge` 查看提示，为了叙述方便省略了调用 `./challenge` 的步骤。

1. `touch flag.txt` 创建一个名为 'flag.txt' 的文件
2. `addgroup rknazo && chgrp rknazo flag.txt` 创建组 'rknazo' 并将文件的组设置为 'rknazo'
3. `adduser -D challenger && chown challenger flag.txt` 创建用户 'challenger' 并将文件的用户设置为 'challenger'
4. `adduser -D ricky && adduser ricky rknazo && adduser challenger rknazo` 创建用户 'ricky' 并将其和 'challenger' 添加到组 'rknazo'
5. `chmod o-rwx flag.txt` 移除其他用户的所有权限
6. `chmod u-w flag.txt` 移除用户（challenger）的写入权限
7. `chmod g-r flag.txt` 移除组（rknazo）的读取权限（“我不需要读取权限”，而我（ricky）属于组（rknazo）成员）
8. `chmod g+w flag.txt` 添加组（rknazo）的写入权限

## 补充

有参与者反映不会使用 busybox 的权限设置指令，其实可以自行通过 alpine 的包管理器 `apk` 安装 `coreutils`: `apk add coreutils`
