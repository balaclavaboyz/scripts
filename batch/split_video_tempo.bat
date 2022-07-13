@echo off
echo Desc: Dividir o arquivo de video em tamanho iguais. Ex: 1mb, 2mb, 1024mb...
set /p nome=Nome do arquivo: 
set /p tempo=Tempo de cada segmento(ex:00:01:00;hh:mm:ss): 
ffmpeg.exe -i "%nome%" -c copy -map 0 -segment_time %tempo% -f segment -reset_timestamps 1 output%%03d.mp4
pause
