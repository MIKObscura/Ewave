# Ewave
This is an EFL based music player I decided to make to learn how to use this library because I think it looks good.  
For now it's still in early development so it only has the basics of a music player.  
To use it, launch `main.py` with your python interpreter, then click the select folder button and pick a directory that contains audio files, all the audio files in that directory will be put inside a play queue which will be used to control what's playing.

# Requirements
A few things are needed in order for the program to run, the python packages are in requirements.txt but there are other dependencies:
* Python 3
* Enlightenment Foundation Libraries (EFL) 1.17<=, the python-efl package is actually just bindings so you'll need to install this too for it to work, this program 
was tested with version 1.26 but normally older versions should work as long as they're still maintained.
* VLC 3.0<=, used by efl for audio playback, again older versions should work but this program was tested with version 3.0.18.

Placeholder image is from: https://openclipart.org/detail/202377/raseone%20record%201