# ModBridge

ModBridge is a small .exe file that you can use to launch any other .exe instead of the original Game.exe which Steam would launch.

***Its most important feature is that Steam Overlay and Playtime tracking will work with your mods!***

It's intended for use with standalone mods or ModOrganizer. Based on simple Python script.

## Instructions

Please read these Instructions, and also the instructions inside ModBridge.ini

> ⚠️ Disable Steam Cloud saves for chosen games, im not sure if it will put different save files in there

1. Compile your own EXE file or use the release version of ModBridge.exe
2. Get ModBridge.ini from this Github
3. **Put both files in the games EXE directory** (sometimes \game\bin\ or sth like that)
4. Know which exe gets launched by Steam (Launch and check in TaskManager)
5. Rename GAME.exe to sth like GAME_backup.exe
7. Now Rename the ModBridge.exe to GAME.exe
8. Make sure you have ModBridge.ini in this same directory
9. In ModBridge.ini set the Target .exe file and optional launch arguments (Check examples below)
10. Launch the original GAME in Steam, the Target.exe will launch and have SteamOverlay working!
---
### Examples of ModBridge.ini

#### XWVM - Amazing Mod for Star Wars: X-Wing (1994)
Point the Target to xwvm.exe
```ini
[Mod]

Target = D:\GAMES\SteamGames\steamapps\common\STAR WARS X-Wing\XWVM\xwvm.exe
WorkDir = 
Args = 
InheritArgs = true
Wait = true
```
#### Stalker G.A.M.M.A. - Amazing Modpack for Stalker Anomaly
1. I choose Stalker CoP in Steam to launch Gamma.
2. Replace the xrEngine.exe in \bin\ with ModBridge
3. Select Gammas ModOrganizer.exe in your ModBridge.ini Target
4. Finally track your hours of playing Gamma!

```ini

[Mod]

Target = E:\GAMMA\ModOrganizer.exe
WorkDir = 
Args = 
InheritArgs = true
Wait = true
```
## Build Instructions
Make sure you have python installed and then get PyInstaller:
```
py -m pip install pyinstaller
```
Download source, then, in the ModBridge source directory:
```
py -m PyInstaller --onefile --noconsole --name ModBridge --icon icon.ico  ModBridge.py
```
This will "compile" and place the ModBridge.exe in ```dist``` folder.
