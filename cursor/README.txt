Slackworld cursor theme
=======================

One multi-resolution Xcursor theme containing native 16, 24, 32, 48 and
64 pixel images, modern cursor names, legacy X11 names and compatibility
hash aliases. Static and animated assets are generated reproducibly by the
source builder.

Install for one user:
  mkdir -p ~/.icons
  cp -a Slackworld ~/.icons/

Install system-wide:
  sudo cp -a Slackworld /usr/share/icons/

Xfce:
  Settings Manager -> Mouse and Touchpad -> Theme -> Slackworld

Manual Xresources fallback:
  Xcursor.theme: Slackworld
  Xcursor.size: 24

Rebuild from source:
  python3 source/build_slackworld_cursor.py

Build requirements:
  Python 3, Pillow, xcursorgen

The generated theme inherits Adwaita only as a final fallback for cursor
names not covered by Slackworld.
