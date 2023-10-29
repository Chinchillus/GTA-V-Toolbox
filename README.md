# Current features:
- Changing languages (English and Polish are currently supported)
- Auto creating dlclist
- Asynchronously moving mod files* from GTA V folder and into it

The dlclist is created and ready to copy, function under button "dc"\

It moves only files that AREN'T in the default file list, for example it will move "mods" folder and "ScriptHookV.dll" from the game folder, but it will not touch "x64.rpf" and other archives (keep in mind if you modded archives OUTSIDE of the mods folder, it will not work because it skips folders and files by their names, it cant detect that you modded an archive outside of the mods folder)

# Planned features and things to do
- Auto unpacking and installing addon mods
- Complete rewrite it in C#

# FAQ
- Why does it show viruses when scanned in virustotal?\
I "compile" or rather repack it to exe using PyInstaller, i can't do anything about it, you can "compile" it yourself if you want

- Why does it take so long to start?\
It is repacked using "onefile" mode in PyInstaller, it firstly needs to unpack the files into temp and then run them  

- What does "sw" and "dc" mean?\
sw - swap\
dc - dlclist creator 


# License
This repository uses MIT License 

Learn more on: https://choosealicense.com/licenses/mit/
