# rknazo-2024

2024 年的一场跨年 CTF 夺旗赛活动！有 Docker 即可参与！

题目难度不高，会用 Linux 就基本能做。

- 奖励：支付宝拼手气口令红包 `30 CNY/50 pcs`
- 开始时间：`2023.12.31 23:00 CST`
- 结束时间：口令红包领取完毕/截止时（`2024.1.1 22:30 CST`）

## 参与方法

1. 在设备上安装 Docker
2. `docker run -it ricky8955555/rknazo-2024:latest` 运行容器
3. 进入容器后 `cat readme.txt` 阅读须知

## 目录结构

```
/
├── build           -  构建工具
├── challenges      -  题目源代码
├── data            -  数据
├── out             -  构建产物
├── solver          -  解题工具
└── Dockerfile      -  Docker 镜像构建配置
```

## 题目

1. [hide_and_seek](challenges/1/)
2. [easy_encoding](challenges/2/)
3. [binary](challenges/3/)
4. [shortcut](challenges/4/)
5. [perm](challenges/5/)
6. [site](challenges/6/)
7. [capture](challenges/7/)
8. [sock](challenges/8/)

题目设计及题解均写于各题目的 readme.md
