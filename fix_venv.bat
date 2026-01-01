@echo off
echo Fechando processos do Python que possam estar usando o .venv...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo Removendo ambiente virtual antigo...
rmdir /s /q .venv 2>nul

echo Criando novo ambiente virtual...
python -m venv .venv

echo Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo Instalando dependencias...
python -m pip install --upgrade pip
pip install langchain_openai python-dotenv

echo.
echo ========================================
echo Ambiente virtual configurado com sucesso!
echo ========================================
echo.
echo Para usar, execute: .venv\Scripts\activate
pause
