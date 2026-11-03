@echo off
chcp 65001 >nul
title 清理旧版 LA_ 打印机（AD-批量打印）
echo.
echo   AD-批量打印：清理旧版本（V2.2.10 及更早）留下的 LA_* 绘图仪
echo   ------------------------------------------------------------------
echo   * 会先完整备份到 D:\批量打印\_backup_LA_userconfig_日期时间\
echo   * 再把原文件挪到各 Plotters 目录下的 "_LA_已清理" 子目录（可还原）
echo   * 只处理 LA_ 开头的 pc3 / pc5 / pmp，不动其它任何文件
echo.
echo   建议先关闭 CAD，避免文件被占用。
echo.
pause

set PY=C:\Users\Administrator\.workbuddy\binaries\python\envs\default\Scripts\python.exe
if not exist "%PY%" set PY=python

"%PY%" "D:\批量打印\清理旧版LA打印机.py"
echo.
pause
