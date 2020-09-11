// installer shell object
//
// $Id$

#ifndef __SHELL_TOONTOWNINSTALLER_H__
#define __SHELL_TOONTOWNINSTALLER_H__

#include <vos/iut/shell.hpp>

class ToontownInstaller : public InstallerShell<RegistryData>
{
public:
	ToontownInstaller();
};

#endif
