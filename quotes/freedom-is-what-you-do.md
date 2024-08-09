---
tag: dailyquote
---

#dailyquote

# Daily Quote

### Freedom is what you do with what's been done to you. ^quote
*-Jean-Paul Sartre* ^author


### Sudo
*/etc/sudoers*

```sh
# This file MUST be edited with the 'visudo' command as root.
#
# Please consider adding local content in /etc/sudoers.d/ instead of
# directly modifying this file.
#
# See the man page for details on how to write a sudoers file.
```

```sh
Defaults        env_reset
Defaults        mail_badpass
Defaults        secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
Defaults        timestamp_timeout=30

# Cmnd alias
# Basic (low priv) commands
Cmnd_Alias      BASIC = /usr/bin/apt, /path/to/other, ...
# Admin commands
Cmnd_Alias      ADMIN = /usr/bin/passwd, /path/to/other, ...

# USERS
root    ALL=(ALL:ALL) ALL # REQUIRED

# User can run all with passwd
user   ALL=(ALL:ALL) ALL
# User can run commands without pass
user   ALL=(ALL:ALL) NOPASSWD: BASIC, ADMIN
# Group can run all with passwd
%group   ALL=(root:ALL) ALL
# Group can run commands without pass
%group   ALL=(root:ALL) NOPASSWD: BASIC

@includedir /etc/sudoers.d
```

```sh
# As of Debian version 1.7.2p1-1, the default /etc/sudoers file created on
# installation of the package now includes the directive:
#
#       #includedir /etc/sudoers.d
#
# This will cause sudo to read and parse any files in the /etc/sudoers.d
# directory that do not end in '~' or contain a '.' character.
#
# Note that there must be at least one file in the sudoers.d directory (this
# one will do), and all files in this directory should be mode 0440.
#
# Note also, that because sudoers contents can vary widely, no attempt is
# made to add this directive to existing sudoers files on upgrade.  Feel free
# to add the above directive to the end of your /etc/sudoers file to enable
# this functionality for existing installations if you wish!
#
# Finally, please note that using the visudo command is the recommended way
# to update sudoers content, since it protects against many failure modes.
# See the man page for visudo for more information.
```
