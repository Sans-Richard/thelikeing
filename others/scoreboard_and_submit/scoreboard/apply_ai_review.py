#!/usr/bin/env python3
"""AI 审查分析写回 data.json。

提交后，AI 读取 reports/<sid>/summary.json + 提交结果，生成审查分析文本，
通过本脚本写入 submission.ai_analysis（仅本地 data.json，远程脱敏不推）。

用法：
  python3 apply_ai_review.py <sid> --analysis "分析文本"
  python3 apply_ai_review.py <sid> --file /path/to/analysis.txt
  python3 apply_ai_review.py <sid> --clear        # 清空审查
"""
import argparse
import json
import os
import sys

DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')


def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('sid')
    ap.add_argument('--analysis')
    ap.add_argument('--file')
    ap.add_argument('--clear', action='store_true')
    args = ap.parse_args()

    data = load_data()
    sub = next((s for s in data['submissions'] if s.get('id') == args.sid), None)
    if not sub:
        print(f'ERROR: submission {args.sid} 不存在')
        sys.exit(1)

    if args.clear:
        sub['ai_analysis'] = None
    elif args.file:
        with open(args.file) as f:
            sub['ai_analysis'] = f.read()
    elif args.analysis:
        sub['ai_analysis'] = args.analysis
    else:
        ap.error('必须提供 --analysis / --file / --clear 之一')

    save_data(data)
    print(f'✓ ai_analysis 已写入 submission {args.sid}')


if __name__ == '__main__':
    main()
