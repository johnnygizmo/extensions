SET /P MyVar=<../folder.txt
"%MyVar%\blender.exe" --command extension build
move /Y *.zip ../ 