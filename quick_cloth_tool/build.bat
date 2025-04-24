SET /P MyVar=<../folder.txt
"c:\blender\%MyVar%\blender.exe" --command extension build
move /Y *.zip ../ 