@echo off
setlocal enabledelayedexpansion
mode con cols=94 lines=30&color 0a&title 创建RPT V3.0 快捷方式
echo.
echo RPT
echo  版本：V3.0
echo  by Rml@dr0n1
echo.
echo [+] 获得当前路径:%~dp0
echo.
echo [+] 开始创建快捷方式...
echo.

rem 设置程序的完整路径(必要)
set Program=%~dp0start.vbs
rem 程序工作路径
set WorkDir=%~dp0
rem 设置快捷方式说明
set Desc=RPT V1.0
rem 设置快捷方式图标
set icon=%~dp0styles\logo.ico

if not defined WorkDir call:GetWorkDir "%Program%"
(
    echo Set WshShell = CreateObject("WScript.Shell"^)
    echo strDesktop = WshShell.SpecialFolders("Desktop"^)
    echo Set oShellLink = WshShell.CreateShortcut(strDesktop ^& "\RPT V3.0.lnk"^)
    echo oShellLink.TargetPath = "%Program%"
    echo oShellLink.WorkingDirectory = "%WorkDir%"
    echo oShellLink.WindowStyle = 1
    echo oShellLink.Description = "%Desc%"
    echo oShellLink.IconLocation = "%icon%"
    echo oShellLink.Save
) > makelnk.vbs

cscript //nologo makelnk.vbs
del /f /q makelnk.vbs

echo [+] 桌面快捷方式创建成功!!
echo.
exit

:GetWorkDir
set WorkDir=%~dp1
set WorkDir=%WorkDir:~0,-1%