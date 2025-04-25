import argparse

from tongban_report.utils.func_report import gen_report
# from utils.safe_report import gen_report

sheet = 'Sheet1'

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="报告生成工具")
    parser.add_argument('-d', '--data', required=True, help='数据来源Excel文件的路径(必填)')
    parser.add_argument('-t', '--template', required=True, help='模板文件Docx文件的路径(必填)')
    args = parser.parse_args()
    print("数据来源:", args.data)
    print("模板文件:", args.template)
    # print("项目类型:", args.project)

    gen_report(docx=args.template, xlsx=args.data, sheet=sheet, project_num=2)
    # gen_report(docx=args.template, xlsx=args.data, sheet=sheet, project_num=2)

if __name__ == "__main__":
    main()
