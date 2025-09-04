Set WshShell = CreateObject("WScript.Shell")

WshShell.Run "cmd.exe /c ""venv\Scripts\activate.bat && python Main.py""", 0, False 

' WshShell.Run "cmd.exe /k ""venv\Scripts\activate.bat && python Main.py""", 1, True 

' /c means carry out the command and then terminate, /k means carry out the command and then remain
' 0 means hide the window, 1 means show the window
' False means don't wait for the command to finish, True means wait for the command to finish
