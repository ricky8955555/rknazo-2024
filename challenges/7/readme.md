# capture

本题考验网络抓包。

## 解题过程

1. `cat flag.txt` 查看提示可猜测有进程在向广播地址发送数据
2. `tcpdump -X` 即可得到 flag
