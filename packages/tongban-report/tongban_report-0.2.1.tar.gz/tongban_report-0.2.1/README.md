### tongban_report

### 通办信息报告生成工具

### 安装
```commandline
pip install tongban_report

pip install --upgrade tongban_report
```

### 使用
```commandline
tongban_report [-h] -d DATA [-f FUNC] [-s SAFE]
options:
  -h, --help       show this help message and exit
  -d, --data DATA  数据来源Excel文件的路径(必填)
  -f, --func FUNC  功能测试报告模板
  -s, --safe SAFE  安全测试报告模板
```

- [x] 给定参数[-f]会生成功能测试报告;
- [x] 给定参数[-s]会生成安全测试报告;
- [x] 同时给定, 将同时生成两份报告;

示例：
> D:\test>tongban_report -d=d:\test\2.xlsx -f=d:\test\functional_input.docx -s=d:\test\safety_input.docx

### 结束