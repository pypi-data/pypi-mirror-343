import argparse

from utils import func_report
from utils import safe_report

sheet = 'Sheet1'

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="报告生成工具")
    parser.add_argument('-d', '--data', required=True, help='数据来源Excel文件的路径(必填)')
    parser.add_argument('-t', '--template', required=True, help='模板文件Docx文件的路径(必填)')
    # parser.add_argument('-p', '--project', help='项目类型(可选,默认为2): 2|20|22|24|4')
    args = parser.parse_args()
    print("数据来源:", args.data)
    print("模板文件:", args.template)
    # print("项目类型:", args.project)

    func_report.gen_report(docx=args.template, xlsx=args.data, sheet=sheet, project_num=2)
    safe_report.gen_report(docx=args.template, xlsx=args.data, sheet=sheet, project_num=2)

if __name__ == "__main__":
    main()
