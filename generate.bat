del *.zip
del *.json
del *.html


cd create_empty_vertex_child
call build.bat
cd ..
cd quick_cloth_tool
call build.bat
cd ..



"c:\blender\blender-4.5.0-alpha+main.5a2a6da0a27f-windows.amd64-release\blender.exe" --command extension server-generate --repo-dir=./
"c:\blender\blender-4.5.0-alpha+main.5a2a6da0a27f-windows.amd64-release\blender.exe" --command extension server-generate --repo-dir=./ --html