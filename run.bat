@echo off
chcp 65001 > nul
title MediaFlow - محرك تنزيل وإدارة الوسائط

echo ========================================================
echo       MediaFlow - تطبيق تنزيل وإدارة الوسائط
echo ========================================================
echo جارٍ بدء تشغيل المحرك والواجهة...

where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py main.py
    goto end
)

where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python main.py
    goto end
)

echo [خطأ] لم يتم العثور على Python في النظام!
echo يرجى تثبيت Python 3.10 أو أحدث لإكمال التشغيل.
pause

:end
