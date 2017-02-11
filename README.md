# mocorpus
A multilingual corpus collected from gettext .mo files in Debian.

Dependencies:

* Debian testing apt source
* make
* aria2c (for downloading .deb packages)
* apt-file
* GNU parallel
* Python 3

Use `make` to make, prepare 10G of disk.

Then `python3 getparallel.py mocorpus.db <Locale_A> <Locale_B>` to get plain text files.
