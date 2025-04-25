import argparse
import sys

# from functional_report import functional_report
# from safety_report import safety_report

sheet = 'Sheet1'

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="报告生成工具")
    parser.add_argument('-m', '--mode', required=True, help='文档类型(必填): FUNC-功能报告 | SAFE-安全报告')
    parser.add_argument('-d', '--data', required=True, help='数据来源Excel文件的路径(必填)')
    parser.add_argument('-t', '--template', required=True, help='模板文件Docx文件的路径(必填)')
    parser.add_argument('-p', '--project', help='项目类型(可选,默认为2): 2|20|22|24|4')
    args = parser.parse_args()
    print("文档类型:", args.mode)
    print("数据来源:", args.data)
    print("模板文件:", args.template)
    print("模板文件:", args.project)

    project_num = args.project if args.project else '2'

    # if args.mode.upper() == "FUNC":
    #     functional_report(docx=args.template, xlsx=args.data, sheet=sheet, project_num=args.project)
    # elif args.mode.upper() == "SAFE":
    #     safety_report(docx=args.template, xlsx=args.data, sheet=sheet, project_num=args.project)
    # else:
    #     print("错误!未知文档类型")
    #     sys.exit(1)

if __name__ == "__main__":
    main()
