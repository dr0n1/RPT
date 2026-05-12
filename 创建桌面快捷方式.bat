@echo off
chcp 65001 >nul
setlocal EnableExtensions DisableDelayedExpansion

set "ScriptDir=%~dp0"
set "MainPy=%ScriptDir%main.py"
set "Program=%ScriptDir%start.vbs"
set "WorkDir=%ScriptDir%"
set "Icon=%ScriptDir%styles\logo.ico"

if not exist "%MainPy%" (
    echo [错误] 未找到 main.py：%MainPy%
    exit /b 1
)

set "Version="
for /f "usebackq tokens=1* delims=:" %%A in (`findstr /b /c:"# @Version:" "%MainPy%"`) do (
    set "Version=%%B"
    goto ReadVersionDone
)

:ReadVersionDone
if not defined Version (
    echo [错误] 未能从 main.py 读取版本号
    exit /b 1
)

for /f "tokens=* delims= " %%A in ("%Version%") do set "Version=%%A"

set "Desc=RPT %Version%"
set "LinkName=RPT %Version%.lnk"

if not exist "%Program%" (
    echo [错误] 未找到启动脚本：%Program%
    exit /b 1
)

if not exist "%Icon%" (
    echo [警告] 未找到图标文件，将使用默认图标：%Icon%
)

mode con cols=94 lines=30
color 0a
title 创建 RPT %Version% 快捷方式

echo.
echo RPT
echo  版本：%Version%
echo  作者：Rml@dr0n1
echo.
echo [信息] 当前路径：%ScriptDir%
echo [信息] 开始创建桌面快捷方式...
echo.

for /f "delims=" %%D in ('powershell -NoProfile -ExecutionPolicy Bypass -Command "[Environment]::GetFolderPath('Desktop')"') do set "DesktopDir=%%D"

if not defined DesktopDir (
    echo [错误] 未能获取当前用户桌面路径
    exit /b 1
)

echo [信息] 桌面路径：%DesktopDir%
echo [信息] 正在删除旧的 RPT 快捷方式...
del /f /q "%DesktopDir%\RPT*.lnk" >nul 2>nul

set "PROGRAM_PATH=%Program%"
set "WORK_DIR=%WorkDir%"
set "SHORTCUT_DESC=%Desc%"
set "ICON_PATH=%Icon%"
set "LINK_NAME=%LinkName%"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$ErrorActionPreference='Stop';" ^
    "$desktop=[Environment]::GetFolderPath('Desktop');" ^
    "$linkPath=Join-Path $desktop $env:LINK_NAME;" ^
    "$shell=New-Object -ComObject WScript.Shell;" ^
    "$shortcut=$shell.CreateShortcut($linkPath);" ^
    "$shortcut.TargetPath=$env:PROGRAM_PATH;" ^
    "$shortcut.WorkingDirectory=$env:WORK_DIR;" ^
    "$shortcut.WindowStyle=1;" ^
    "$shortcut.Description=$env:SHORTCUT_DESC;" ^
    "if (Test-Path -LiteralPath $env:ICON_PATH) { $shortcut.IconLocation=$env:ICON_PATH };" ^
    "$shortcut.Save();"

set "CreateResult=%ERRORLEVEL%"

if "%CreateResult%"=="0" goto CreateSuccess

echo [错误] 桌面快捷方式创建失败，错误码：%CreateResult%
exit /b %CreateResult%

:CreateSuccess
echo [成功] 桌面快捷方式创建成功！
echo.
exit /b 0