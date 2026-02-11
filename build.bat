SET /P MyVar=< ../extensions/folder.txt
"%MyVar%\blender.exe" --command extension build
move /Y *.zip ../extensions/ 