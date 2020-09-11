
SIGN_DIR := ${WINTOOLS}/sdk/ms_platform_sdk/Bin
VERISIGN_DIR := //cred.wdig.com/verisign_credentials/WaltDisneyCompany
ACTIVEX_NAME := ttinst

TESTSERVER_NAME :=
BUILD_SUFFIX :=
signname :=

include product_release.mk

ifneq '${LANGUAGE}' 'english'
	BUILD_SUFFIX := -${LANGUAGE}
	ACTIVEX_NAME := $(ACTIVEX_NAME)-${LANGUAGE}
	signname += $(shell perl -e "print ucfirst(${LANGUAGE})")
endif

#nothing:
#	@echo "building for: $(PRODUCT_RELEASE)"

cab_cmd := $(SIGN_DIR)/Cabarc -s 6144 n $(ACTIVEX_NAME).cab $(ACTIVEX_NAME).dll $(ACTIVEX_NAME).inf
#sign_cmd := $(SIGN_DIR)/signcode -spc $(VERISIGN_DIR)/mycredentials.spc -v $(VERISIGN_DIR)/myprivatekey.pvk -n \"Toontown$(TESTSERVER_NAME) Installer$(signname)\" -t http://timestamp.verisign.com/scripts/timstamp.dll $(ACTIVEX_NAME).cab

#BUILDMODE := Debug
BUILDMODE := Release

digisign = $(SIGN_DIR)/signcode -spc $(VERISIGN_DIR)/mycredentials.spc -v $(VERISIGN_DIR)/myprivatekey.pvk -n "Toontown$(TESTSERVER_NAME) Installer$(signname)" -t http://timestamp.verisign.com/scripts/timstamp.dll $(notdir $(1))
#
# remember, UPX compression strips debug info
#ifeq '$(BUILDMODE)' 'Debug'
#	upx_compress = echo 0
#else
	upx_compress = ${WINTOOLS}/built/bin/upx --brute -f $(notdir $(1))
#endif
#
# 2008/04/03: can't use UPX compress binaries that elevate to admin in Vista?!
#
#create_manifest = ${WINTOOLS}/sdk/ms_platform_sdk/Bin/winnt/mt.exe -verbose -manifest "$(1)" -out:"$(1).gen";\#1
embed_manifest = ${WINTOOLS}/sdk/ms_platform_sdk/Bin/winnt/mt.exe -manifest "$(1)" -outputresource:"$(2);1"

ifneq '${PPREMAKE_PLATFORM}' ''
odir_platform := ${PPREMAKE_PLATFORM}
endif
odir_platform ?= Cygwin

BASE_DIR := ${TOONTOWN}/src
BUILD_DIR := $(BASE_DIR)/installer/Opt4-$(odir_platform)$(BUILD_SUFFIX)
HELPER_DIR := $(BASE_DIR)/installer/standalone/win32/$(BUILDMODE)
SVC_DIR := $(BASE_DIR)/installer/service/win32/$(BUILDMODE)
INSTALLER_DIR := $(BASE_DIR)/launcher

VOS_BASE_DIR := ${TOONTOWN}/../vos

HELPER_NAME := ttinst-helper.exe
SERVICE_NAME := wdigInstallerSvc.exe
INSTALLER_NAME := InstallLauncher.exe

INSTALLER_PATH := $(INSTALLER_DIR)/$(INSTALLER_NAME)
#INSTALLER_MANIFEST := $(INSTALLER_PATH).manifest

SETUP_NAME := ttinst-setup$(PRODUCT_RELEASE).exe

all: $(BUILD_DIR) .cab-sign .setup-sign .checksum-gen
#   	.helper-build .svc-build .setup-build .setup-sign $(BUILD_DIR)/$(ACTIVEX_NAME).cab .checksum-gen bootstrap

$(BUILD_DIR):
	mkdir -p $@

resign:
	rm .cab-sign .helper-sign .svc-sign .setup-sign
	$(MAKE) -f vista.mk .cab-sign .helper-sign .svc-sign .setup-sign

rebuild:
	rm .helper-sign .svc-sign .setup-sign .checksum-gen

$(BUILD_DIR)/$(ACTIVEX_NAME).cab: $(BUILD_DIR)/$(ACTIVEX_NAME).inf $(BUILD_DIR)/$(ACTIVEX_NAME).dll
	cd $(BUILD_DIR) && $(cab_cmd)

.cab-sign: $(BUILD_DIR)/$(ACTIVEX_NAME).cab
	cd $(BUILD_DIR) && $(call digisign, $<)
	@touch $@

$(BUILD_DIR)/$(HELPER_NAME): $(HELPER_DIR)/$(HELPER_NAME)
	cp $< $(BUILD_DIR)

$(BUILD_DIR)/$(SERVICE_NAME): $(SVC_DIR)/$(SERVICE_NAME)
	cp $< $(BUILD_DIR)

.helper-sign: $(BUILD_DIR)/$(HELPER_NAME)
ifneq '$(BUILDMODE)' 'Debug'
	cd $(BUILD_DIR) && $(call upx_compress,$(HELPER_NAME))
endif
	cd $(BUILD_DIR) && $(call digisign,$(HELPER_NAME))
	@touch $@

.svc-sign: $(BUILD_DIR)/$(SERVICE_NAME)
	cd $(BUILD_DIR) && $(call digisign,$(SERVICE_NAME))
	@touch $@

$(BUILD_DIR)/$(SETUP_NAME): .helper-sign .svc-sign
	make -C bootstrap

.setup-sign: $(BUILD_DIR)/$(SETUP_NAME)
	cd $(BUILD_DIR) && $(call digisign,$(SETUP_NAME))
	@touch $@

.checksum-gen: .setup-sign $(BUILD_DIR)/$(ACTIVEX_NAME).cab
	bin/calc_md5.pl $(BUILD_DIR)/$(HELPER_NAME) > $(BUILD_DIR)/bootstrap.db
	bin/calc_md5.pl $(BUILD_DIR)/$(SERVICE_NAME) >> $(BUILD_DIR)/bootstrap.db
	bin/calc_md5.pl $(BUILD_DIR)/$(SETUP_NAME) >> $(BUILD_DIR)/bootstrap.db
	@touch $@

$(BUILD_DIR)/$(INSTALLER_NAME).RES: $(INSTALLER_PATH).rc $(INSTALLER_PATH).manifest
	cp $? $(BUILD_DIR)
	cd $(BUILD_DIR) && rc /r $(notdir $<)

ship: .checksum-gen .setup-sign .cab-sign
	bin/pubax.sh

#.wise-manifest: $(INSTALLER_PATH) $(BUILD_DIR)/$(INSTALLER_NAME).RES
#	cp $< $(BUILD_DIR)
#	cd $(BUILD_DIR) && link $(notdir $^) /out:$(notdir $<).test
#	cd $(CURDIR)/$(BUILD_DIR) && $(call embed_manifest,InstallLauncher.exe.manifest,InstallLauncher.exe)
#	@cp -u $(BUILD_DIR)/$(notdir $<) /c/publish-web/download/portuguese/currentVersion
#	touch .wise-manifest
