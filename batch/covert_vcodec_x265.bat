@echo off
set /p nome=Nome do arquivo: 
ffmpeg.exe -i %nome% -vcodec libx265 -crf 28 compressed_%nome%
pause
