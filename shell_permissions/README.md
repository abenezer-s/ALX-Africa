# shell permissions.
su betty - switch current user to betty.

whoami - command that outputs current user.

touch hello - creat a new file named hello.

chmod u+x hello - give owner of hello execute permissions.

chmod u=rwx,g=rx,o=r hello - give owner read, write and execute permissions, group read and execute and others read permissions.

chmod 753 hello - give rwx permission for owner, rx permmisions for group and wx for others.

