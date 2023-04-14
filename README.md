# Ewave
![screenshot](https://cdn.discordapp.com/attachments/1045329788295983137/1096411538165870602/image.png)
This is a basic EFL based music player. Nothing fancy, just pick files/directories and play!
For now it's still in early development so it only has the basics of a music player.  
To use it, launch `main.py` with your python interpreter, then click on one of the buttons in the top right to pick an option to populate the play queue, there are 4 at the moment:
- Pick directory: select a directory that contains audio files, all the audio files in that directory will be put in the play queue
- Pick playlist: select a text file that defines a playlist, these files should contain absolute paths to audio files, one per line
- Pick cue: select a cue sheet, the file associated with that sheet will be the play queue
- Add to queue: select a file and add it to the play queue [Note: doesn't work if you picked a cue before]  
There is also a View Queue button, this opens a window containing a list of the tracks in the playing queue (the currently playing track is shown in bold), you can drag tracks around if you want to change the order manually

# Requirements
A few things are needed in order for the program to run, the python packages are in requirements.txt but there are other dependencies:
* Python 3
* Enlightenment Foundation Libraries (EFL) 1.17<=, the python-efl package is actually just bindings so you'll need to install this too for it to work, this program 
was tested with version 1.26 but normally older versions should work as long as they're still maintained.
* VLC 3.0<=, used by efl for audio playback, again older versions should work but this program was tested with version 3.0.18.

Placeholder image is from: https://openclipart.org/detail/202377/raseone%20record%201