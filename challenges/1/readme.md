# hide_and_seek

本题使用了 Unix 的 `.` 前缀文件隐藏特性。

## 解题过程

1. `cat flag.txt` 查看提示
2. `ls -a` 找出所有文件
3. `cat .flag.txt` 即可解题
