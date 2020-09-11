Toontown Installer ActiveX Control
==================================
Darren Ranalli, 1.2.2001

This is the readme.txt documentation file for the Toontown Installer ActiveX
Control, for Internet Explorer 4.x and up.

Building
--------
There are several script files that facilitate command-line build operations.
_build will completely rebuild the project from scratch. _make is the
same as _build, but it will only rebuild components that have changed
since the last build. _clean will remove temporary project files. 

Distribution
------------
The Toontown Installer ActiveX Control is distributed in a .cab file. The .cab
file contains two files: ttinst.dll and ttinst.inf. The DLL is the actual
ActiveX control, and the .inf file contains information that allows Internet
Explorer to install and update the control. The .cab file is also compressed,
which helps reduce download time.

The .cab file is digitally signed with WDI's credentials using a utility program
called cabarc.exe. Look at publish.bat and sign.bat to see how the signing is
performed. None of the files required for signing are included in revision
control, they should be kept local for security reasons.

Publishing
----------
The project is set up to conditionally "publish" the ActiveX control after
every build operation. Publishing consists of packaging the .dll and .inf
files into a .cab file, signing the cab file, and copying the .cab file
to a particular location, along with several .htm files. Publishing will only
take place if a file called "publish" is present in the project directory.
The size and contents of the "publish" file do not matter.

The batch file that is run after each build is called postbuild.bat. It looks
for the "publish" file, and if it is not found, it does nothing. Otherwise,
it calls publish.bat with a single argument -- the directory to publish to.

publish.bat packages the files into a .cab file, calls sign.bat to sign the
.cab file, and copies it, along with several .htm files, to the publish
directory.

sign.bat attempts to sign the .cab file. It opens a password dialog every
time. For security reasons, I will not put the password here. Ask Darren,
Mike, or Joe for it.

Versioning
----------
When a new release of the control is ready to be built and posted to the
server, there are three version numbers that need to be changed:

1) The version number of the control is found in the VS_VERSION_INFO
version resource. To edit this resource, open the project in VC++ and
look in the Resources dialog. There are two copies of the version number,
labeled "FILEVERSION" and "PRODUCTVERSION". These two version numbers
should always be the same. For each new release, the version number should
be made larger. Remember that numbers on the left have more significance
than numbers on the right; for instance, 0,0,1,0 is larger than 0,0,0,1.
NOTE: This can also be done by hacking the installer.rc file directly. Be
sure to change all *four* (4) copies of the version number in the .rc file.

2) The second place where the version needs to be updated is in the file
"ttinst.inf". There is a line that starts with "FileVersion=", which is
followed by the version number.

3) The third and final place where the version needs to be updated is in
$TOONTOWN/src/web/www/toontownInstallerObject.inc. Search in the file for
the string "ttinst.cab#Version=". This should be followed by the version
number.

For normal releases, all three of these version numbers should be identical.
For debugging purposes, IE can be tricked into always re-installing the
ActiveX control. To do this, simply make version numbers 2) and 3) identical
and larger than version number 1).

Uninstall
---------
To remove the ActiveX control from your system, locate the "Downloaded Program
Files" directory (usually directly under the Windows directory) and delete the
"Toontown Installer ActiveX Control" entry.

Automated Uninstall
-------------------
Run 'Configrc.exe -uninstall_activex'.  This is done automatically
by the wise uninstaller

Debug
-----
There is a Build Configuration called "INSTALLER_DEBUG Release MinDependency". This
configuration spawns the launcher in debug mode. This second Build Configuration is a
copy of the "Release MinDependency" Build Configuration, with the following
modifications:

_INSTALLER_DEBUG is defined under
Project->Settings->C/C++->Category->Preprocessor->Preprocessor Definitions.

the postbuild step passes "-d" to postbuild.bat

Other future project settings modifications should be done using both Build Configurations,
by choosing "Settings for Multiple Configurations" before making the changes. If
the Configurations get out of sync, delete the INSTALLER_DEBUG Configuration, create
it again from Release MinDependency, and re-perform the above modifications.









