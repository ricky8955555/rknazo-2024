# shortcut

本题使用了 Unix 符号链接特性。

## 解题过程

1. `cat flag.txt` 会发现提示 `cat: can't open 'flag.txt': No such file or directory`
2. `cat hint.txt` 查看提示并经过思考或尝试，可发现在 `ls -l` 中显示 `flag.txt` 为一个符号链接
3. `readlink flag.txt` 可看到链接目标有 Hex 特性
4. `readlink flag.txt | xxd -r -p` 即可得到结果
