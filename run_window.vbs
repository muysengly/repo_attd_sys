Set oWS = WScript.CreateObject("WScript.Shell") 
sLinkFile = oWS.CurrentDirectory & "\run_window.lnk" 
Set oLink = oWS.CreateShortcut(sLinkFile)    
oLink.TargetPath = oWS.CurrentDirectory & "\venv\Scripts\python.exe" 
oLink.Arguments = oWS.CurrentDirectory & "\Main.py" 
oLink.WorkingDirectory = oWS.CurrentDirectory    
oLink.WindowStyle = 1    
oLink.Description = "Run Attendance System Application" 
oLink.IconLocation = oWS.CurrentDirectory & "\icon.ico" 
oLink.Save 
