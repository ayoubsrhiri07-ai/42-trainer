@echo off
rem Double-clique ici pour lancer 42 Trainer (il s'ouvre dans ton navigateur).
rem Cherche Python lui-meme : marche meme si le PATH de Windows n'est pas a jour.
chcp 65001 >nul
cd /d "%~dp0"
title 42 Trainer
set "PYTHONUTF8=1"
set "PY="
for %%P in (python.exe) do if not "%%~$PATH:P"=="" set "PY=%%~$PATH:P"
if not defined PY for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do if exist "%%D\python.exe" set "PY=%%D\python.exe"
if not defined PY (
  echo Python est introuvable. Installe-le avec : winget install Python.Python.3.13
  pause
  exit /b 1
)
"%PY%" server.py %*
if errorlevel 1 pause
