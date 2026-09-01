SlackWorld GRUB theme
======================

Target directory:
  /boot/grub/themes/slackworld/

Install:
  sudo mkdir -p /boot/grub/themes/slackworld
  sudo cp -a slackworld/. /boot/grub/themes/slackworld/

Set in /etc/default/grub:
  GRUB_THEME="/boot/grub/themes/slackworld/theme.txt"
  GRUB_GFXMODE=1920x1080x32

Then rebuild GRUB's configuration (Slackware):
  sudo grub-mkconfig -o /boot/grub/grub.cfg

Font requirement:
  The theme uses the installed PF2 font whose internal name is
  "Hack Regular 20" (previously confirmed as /boot/grub/fonts/hack.pf2).

Backgrounds:
  slackworld.png       - the user's original Slackware background (default)

Menu assets:
  menu_*.png   - translucent outer menu panel
  item_*.png   - invisible normal-row geometry stabilizer
  select_*.png - visible selected-row highlight
