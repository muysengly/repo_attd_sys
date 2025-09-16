Set WshShell = CreateObject("WScript.Shell")

WshShell.Run "cmd.exe /c venv\Scripts\activate && python Main.py", 0, False