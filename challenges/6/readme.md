# site

本题考验 HTTP 及 DNS 的使用。

## 解题过程

1. `cat flag.txt` 查看提示可猜测使用了 HTTP
2. `curl 127.69.60.1` 可得到进一步提示
3. 根据提示 “你在找的东西藏在了你正在请求的地址的某个服务上, 并且它以某种形式使用了这个地址进行记录.” 可猜测此处使用了 DNS PTR 记录（可通过 `netstat -tuln` 查询端口占用判断）
4. `dig -x 127.69.60.1 @127.69.60.1` 查询 PTR 记录可得其指向 `site.nazo.rk.` 可猜测有信息在 `site.nazo.rk.` 的 TXT 记录上
5. `dig site.nazo.rk. TXT @127.69.60.1` 可得到 flag

## 补充

有参与者反映这题 HTTP 返回的提示有点谜语（x
