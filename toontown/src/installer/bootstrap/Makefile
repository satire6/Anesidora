NSIS := '/c/apps/development/NSIS/makensis.exe'
include ../product_release.mk

nocygTOONTOWN := `/bin/cygpath -w $(TOONTOWN)`
TARGETDIR := ../Opt4-Cygwin-${LANGUAGE}
DEPENDENCIES := installer.nsi \
				$(TARGETDIR)/ttinst-helper.exe \
				$(TARGETDIR)/wdigInstallerSvc.exe
TARGET := ttinst-setup$(PRODUCT_RELEASE).exe

# non-roman language-types need a special file
ifeq '$(LANGUAGE)' 'japanese'
DEPENDENCIES += $(LANGUAGE)/$(LANGUAGE).nsh
endif
ifeq '$(LANGUAGE)' 'portuguese'
DEPENDENCIES += $(LANGUAGE)/$(LANGUAGE).nsh
endif
ifeq '$(LANGUAGE)' 'french'
DEPENDENCIES += $(LANGUAGE)/$(LANGUAGE).nsh
endif

$(TARGETDIR)/$(TARGET): $(DEPENDENCIES)
	@echo building for: $(PRODUCT_RELEASE)
	$(NSIS) /V3 /DPRODUCT_VERSION="1.1" /DPRODUCT_RELEASE="$(PRODUCT_RELEASE)" /DLANGUAGE=$(LANGUAGE) /DTOONTOWN="$(nocygTOONTOWN)" installer.nsi
	mv $(TARGET) $(TARGETDIR)

clean:
	rm -f $(TARGETDIR)/$(TARGET)

