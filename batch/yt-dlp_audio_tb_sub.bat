@echo off
set /p input=input url yt: 
yt-dlp.exe %input% --add-metadata --embed-thumbnail --extract-audio --sub-lang en --embed-subs
pause