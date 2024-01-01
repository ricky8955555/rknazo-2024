# sock

本题使用了 Unix Socket。

## 解题过程

1. `cat flag.txt` 查看提示可猜测需要进行进程间通信，同时结合题目标题可猜测此处使用了 Unix Socket
2. `netstat -xl` 可看到 `/run/rknazo-sock.ctl` 有个 Unix Socket 正在被监听着
3. `nc -U /run/rknazo-sock.ctl` 与 Socket 进行通信
4. 输入 `help` 获取帮助
5. 输入 `flag` 即可获取 flag
