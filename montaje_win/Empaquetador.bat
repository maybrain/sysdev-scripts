XCOPY "C:\Users\UsuarioDell07\Desktop\COPIA AQUI NW\*.*" "C:\Projects\WrapperNodeWebkit\Aula Virtual\Aula Virtual\Resources\" /Y
cd "C:\Projects\WrapperNodeWebkit\Aula Virtual"
rd .\BuildResults /S /Q
md .\BuildResults



REM set msBuildDir=%WINDIR%\Microsoft.NET\Framework\v3.5
set msBuildDir=%WINDIR%\Microsoft.NET\Framework\v4.0.30319
call %msBuildDir%\msbuild.exe  "Aula Virtual.sln" /p:Configuration=Release /l:FileLogger,Microsoft.Build.Engine;logfile=Manual_MSBuild_ReleaseVersion_LOG.log
set msBuildDir=

XCOPY ".\Aula Virtual\Bin\Release\Aula Virtual.exe" .\BuildResults\ 

%SystemRoot%\explorer.exe .\BuildResults\
#pause
