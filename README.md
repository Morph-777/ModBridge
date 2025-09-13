# ModBridge

ModBridge is a small .exe file that you can use to launch any other .exe instead of the original Game.exe which Steam would launch.

***Its most important feature is that Steam Overlay and Playtime tracking will work with your mods!***

It's intended for use with standalone mods or ModOrganizer. Based on simple Python script.

## Instructions

***Please read these Instructions, and also the instructions inside ModBridge.ini  
And check out the Examples below, they might help getting it to work with your game/mod.***

> ⚠️ Disable Steam Cloud saves for chosen games, im not sure if it will confuse different save files

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

##### Multiple Profiles Advanced example:
>**I hope this helps someone to make it work with their desired game.**

I choose Stalker CoP in Steam and add multiple Profiles to launch Vanilla, Gamma and Gunslinger Mod. For this game, we need to perform some additional steps to workaround some of the limitations.
1. Rename ```bin``` folder to ```bin_vanilla```
2. Create new ```bin``` folder
3. Place ModBridge.exe in ```bin``` folder and name it ```xrEngine.exe```, check "Run as Admin" in properties
4. Create new text file called ```steam_appid.txt``` inside ```bin_vanilla```
5. Put steam appid in the txt file, for CoP it is ```41700``` (necessary to fix Steam relaunch loop)
6. Use the ini from the example below, with your own paths
7. Using the profiles, i can switch between mods with Steam Launch arguments, e.g.  "-p Gamma" without quotes, for Gamma Modpack
8. Or i remove steam launch parameter and it will default to Profile [Mod], which is Vanilla version
9. All playtime will count towards Stalker CoP in Steam
10. If you run Steam as admin, Overlay should work

***Running the ModBridge and Steam as Admin is required in this case, because of XRay Engine privilege limitations. You'll know, when you get Privilege Error or Overlay doesn't work.***

```ini
[Mod]
Target      = E:\GAMES\SteamGames\steamapps\common\Stalker Call of Pripyat\bin_vanilla\xrEngine.exe
WorkDir     = E:\GAMES\SteamGames\steamapps\common\Stalker Call of Pripyat
Args = 
InheritArgs = true
Wait        = true

[Gamma]
Target = E:\GAMMA\ModOrganizer.exe
WorkDir = 
Args = 
InheritArgs = true
Wait        = true

[Gunslinger]
Target = E:\GAMES\SteamGames\steamapps\common\Stalker Call of Pripyat\Gunslinger\Play GUNSLINGER Mod.exe
WorkDir = 
Args = 
InheritArgs = true
Wait        = true
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
