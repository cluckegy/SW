@echo off

:: تحميل السكربتات
curl -s -L -o setup.py https://gitlab.com/cluckegy/sw/-/raw/main/setup.py
curl -s -L -o show.bat https://gitlab.com/cluckegy/sw/-/raw/main/show.bat
curl -s -L -o loop.bat https://gitlab.com/cluckegy/sw/-/raw/main/loop.bat


:: تحميل litemanager وفك الضغط
powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.litemanager.com/soft/litemanager_5.zip', 'litemanager.zip')"
powershell -Command "Expand-Archive -Path 'litemanager.zip' -DestinationPath '%cd%'"

:: تثبيت مكتبة pyautogui
pip install pyautogui --quiet

:: تثبيت vcredist
choco install vcredist-all --no-progress

:: تحميل البرامج إلى سطح المكتب
curl -s -L -o C:\Users\Public\Desktop\TOOLBOXLAP.exe https://pkgs.tailscale.com/stable/tailscale-setup-latest.exe
curl -s -L -o C:\Users\Public\Desktop\anydesk.exe https://download.anydesk.com/AnyDesk.exe
curl -s -L -o C:\Users\Public\Desktop\ixBrowser.exe https://cdn.ixbrowser.com/ixbrowser/version/ixBrowser_Setup_2_3_30.exe
curl -s -L -o C:\Users\Public\Desktop\VSCODE.exe https://vscode.download.prss.microsoft.com/dbazure/download/stable/e54c774e0add60467559eb0d1e229c6452cf8447/VSCodeUserSetup-x64-1.97.2.exe
curl -s -L -o C:\Users\Public\Desktop\Winrar.exe https://www.rarlab.com/rar/winrar-x64-621.exe
curl -s -L -o C:\Users\Public\Desktop\WindscribeSetup.exe https://deploy.totallyacdn.com/desktop-apps/2.15.8/Windscribe_2.15.8_amd64.exe
powershell -Command "Invoke-WebRequest 'https://github.com/chieunhatnang/VM-QuickConfig/releases/download/1.6.1/VMQuickConfig.exe' -OutFile 'C:\Users\Public\Desktop\VMQuickConfig.exe'"

:: تثبيت WinRAR بصمت وحذفه
C:\Users\Public\Desktop\Winrar.exe /S
del C:\Users\Public\Desktop\Winrar.exe

:: تثبيت Windscribe بصمت
C:\Users\Public\Desktop\WindscribeSetup.exe /VERYSILENT /NORESTART

:: حذف اختصارات مزعجة
del /f "C:\Users\Public\Desktop\Epic Games Launcher.lnk"
del /f "C:\Users\Public\Desktop\Unity Hub.lnk"

:: تغيير باسورد يوزر
net user runneradmin MoGlitch

:: تشغيل لايت مانجر
start "" "LiteManager Pro - Server.msi"

:: كود بايثون للضغط التلقائي
python -c "import pyautogui as pag; pag.click(897, 64, duration=2)"

:: تشغيل السكربتات
python setup.py

