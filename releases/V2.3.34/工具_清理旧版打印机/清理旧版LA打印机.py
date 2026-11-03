# -*- coding: utf-8 -*-
"""清理 CAD 用户配置里旧版本留下的 LA_* 绘图仪（V2.2.10 及更早的命名）。

行为：
  1) 先在 D:\\批量打印\\_backup_LA_userconfig_<日期>\\ 完整备份；
  2) 备份校验通过后，才把原文件移入同目录下的 _LA_已清理\\ 子目录（可随时还原）；
  3) 全程只处理文件名以 LA_ 开头的 .pc3/.pc5/.pmp，不碰任何其它文件。

用法：
    python 清理旧版LA打印机.py            # 执行（默认带备份）
    python 清理旧版LA打印机.py --dry      # 只列出将要处理的文件
"""
import datetime
import os
import shutil
import sys

ROOTS = [
    os.path.join(os.environ.get('APPDATA', ''), 'Autodesk'),
    os.path.join(os.environ.get('APPDATA', ''), 'ZWSOFT'),
    os.path.join(os.environ.get('APPDATA', ''), 'ZWSOFT', 'ZWCAD'),
    os.path.join(os.environ.get('APPDATA', ''), 'Gstarsoft'),
    os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Autodesk'),
]
TARGET_EXT = ('.pc3', '.pc5', '.pmp')
PREFIX = 'LA_'


def looks_like_plotter(name):
    return name.upper().startswith(PREFIX) and name.lower().endswith(TARGET_EXT)


def collect():
    found = []
    for root in ROOTS:
        if not root or not os.path.isdir(root):
            continue
        for base, dirs, files in os.walk(root):
            for f in files:
                if looks_like_plotter(f):
                    found.append(os.path.join(base, f))
    return sorted(set(found))


def main():
    dry = '--dry' in sys.argv
    files = collect()

    print('=' * 68)
    print('旧版 LA_* 绘图仪清理')
    print('=' * 68)
    if not files:
        print('没有找到需要清理的文件 —— 本机已干净。')
        return 0

    print('找到 %d 个文件：' % len(files))
    for p in files:
        print('   ', p)

    if dry:
        print('\n(--dry 模式：未做任何改动)')
        return 0

    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup = os.path.join('D:\\批量打印', '_backup_LA_userconfig_' + stamp)

    # 1) 备份
    copied = 0
    for p in files:
        drive = os.path.splitdrive(p)[0].replace(':', '')
        dst = os.path.join(backup, drive, os.path.relpath(p, drive + os.sep))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(p, dst)
        copied += 1
    print('\n已备份 %d 个文件 -> %s' % (copied, backup))

    missing = [p for p in files if not os.path.isfile(p)]
    if copied != len(files) or missing:
        print('！！ 备份不完整，已中止，未删除任何文件。')
        return 1

    # 2) 移入同目录下的隔离子目录（保留可还原性）
    moved = 0
    for p in files:
        quarantine = os.path.join(os.path.dirname(p), '_LA_已清理')
        os.makedirs(quarantine, exist_ok=True)
        target = os.path.join(quarantine, os.path.basename(p))
        try:
            if os.path.exists(target):
                os.remove(target)
            shutil.move(p, target)
            moved += 1
        except Exception as e:
            print('   移不动（可能被 CAD 占用，先关掉 CAD 再跑一次）: %s  ->  %s' % (p, e))

    print('\n已隔离 %d / %d 个文件。' % (moved, len(files)))
    print('备份目录：%s' % backup)
    print('被移走的文件在各 Plotters 目录下的 "_LA_已清理" 子目录里，需要还原直接搬回去即可。')

    left = collect()
    print('\n复核：目录里剩余 LA_* 文件 %d 个。' % len(left))
    for p in left:
        print('   ', p)
    if not left:
        print('完成：旧 LA_* 绘图仪已全部清理。')
    return 0


if __name__ == '__main__':
    sys.exit(main())
