import argparse
import sys

from tongban_report.utils.func_report import func_report
from tongban_report.utils.safe_report import safe_report

sheet = 'Sheet1'

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="报告生成工具")
    parser.add_argument('-d', '--data', required=True, help='数据来源Excel文件的路径(必填)')
    parser.add_argument("-f", "--func", help="功能测试报告模板")
    parser.add_argument("-s", "--safe", help="安全测试报告模板")
    args = parser.parse_args()

    print("数据来源:", args.data)

    if args.func:
        print("功能模板:", args.func)
        func_report(docx=args.func, xlsx=args.data, sheet=sheet, project_num=2)
    if args.safe:
        print("安全模板:", args.safe)
        safe_report(docx=args.safe, xlsx=args.data, sheet=sheet, project_num=2)
    if not args.func and not args.safe:
        print("错误：必须指定 -f 或 -s 中的至少一个")
        sys.exit(1)

if __name__ == "__main__":
    main()
