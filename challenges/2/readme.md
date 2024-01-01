# easy_encoding

本题使用了 Base64 进行两次编码。

## 解题过程

1. `cat flag.txt` 查看内容可发现其 Base64 编码特性
2. `cat flag.txt | base64 -d` 可发现解出来内容仍有 Base64 编码特性
3. `cat flag.txt | base64 -d | base64 -d` 便得出最终结果
