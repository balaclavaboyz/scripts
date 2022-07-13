@echo off
setlocal EnableDelayedExpansion
set /p nome=Nome do arquivo: 
echo mkv mp3 mp4 opus ...
set nome_sem_ext=%nome%
set /p ext=Extensão para conversão: 
for /f "delims=. tokens=1,2" %%i in ("%nome_sem_ext%") do set nome_sem_ext=%%i
ffmpeg.exe -i %nome% %nome_sem_ext%.%ext%
pause
