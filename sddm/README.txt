MySlackware SDDM theme (Qt 6)
=============================

Dependencies:
  - SDDM built with Qt 6
  - Qt 6 QtQuick/QML runtime
  - SddmComponents (installed with SDDM)

No KDE Frameworks, Plasma components, icon theme, Qt Graphical Effects,
Qt Multimedia, or external QML packages are used.

Install:
  sudo mkdir -p /usr/share/sddm/themes/myslackware
  sudo cp -a myslackware-sddm/. /usr/share/sddm/themes/myslackware/

Select the theme by creating /etc/sddm.conf.d/theme.conf:
  [Theme]
  Current=myslackware

Preview without logging out (command name can vary by build):
  sddm-greeter-qt6 --test-mode --theme /usr/share/sddm/themes/myslackware

If only sddm-greeter exists:
  sddm-greeter --test-mode --theme /usr/share/sddm/themes/myslackware

Customize theme.conf.user instead of theme.conf to preserve local settings:
  [General]
  background=myslackware.png
  fontFamily=Hack
  welcomeText=Welcome to the world of Slackware Linux

Before enabling the theme, run the preview command from a graphical terminal.
Do not restart a running SDDM session unless you are prepared to be logged out.

In standalone test mode there is no daemon socket. Socket warnings and failed
login writes are expected; login and power actions intentionally do nothing.
The restart and shutdown controls remain visible for visual inspection.

Official reference:
  https://github.com/sddm/sddm/blob/develop/docs/THEMING.md
