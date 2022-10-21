@echo off

call %~dp0telegram_bot\venv\Scripts\acivate

cd %~dp0telegram_bot

set TOKEN=5437982372:AAGfwljaVDD2-TC7kYy2Pcr_7zxWlwNzmc4

python test.py

pause 