# Ewave
This is an EFL based music player I decided to make to learn how to use this library because I think it looks good.  
For now it's still in early development so it only has the basics of a music player.  
To launch it, give the absolute path to an audio file to the `FILE` variable in `main.py` then launch it with your python interpreter

# Requirements
A few things are needed in order for the program to run, the python packages are in requirements.txt but there are other dependencies:
* Python 3
* Enlightenment Foundation Libraries (EFL) 1.17<=, the python-efl package is actually just bindings so you'll need to install this too for it to work, this program 
was tested with version 1.26 but normally older versions should work as long as they're still maintained.
* VLC 3.0<=, used by efl for audio playback, again older versions should work but this program was tested with version 3.0.18.

Placeholder image is from: https://openclipart.org/detail/202377/raseone%20record%201