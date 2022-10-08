SHELL = /bin/bash

PACKAGE_NAME=exam_notifier
DIST_ROOT_PATH=build/dist
SOURCE_ROOT_PATH=src/$(PACKAGE_NAME)
ASSETS_TARGET_PATH=$(SOURCE_ROOT_PATH)/gui/assets

SOURCE_FOLDER = src/
TEST_FLAGS ?= -n4
DIST_TYPE ?= local
BUILD_TARGET ?= current

# Show help message
help:
	@echo "$$(tput bold)Available targets:$$(tput sgr0)";echo;sed -ne"/^# /{h;s/.*//;:d" -e"H;n;s/^# //;td" -e"s/:.*//;G;s/\\n# /---/;s/\\n/ /g;p;}" ${MAKEFILE_LIST}|LC_ALL='C' sort -f|awk -F --- -v n=$$(tput cols) -v i=19 -v a="$$(tput setaf 6)" -v z="$$(tput sgr0)" '{printf"%s%*s%s ",a,-i,$$1,z;m=split($$2,w," ");l=n-i;for(j=1;j<=m;j++){l-=length(w[j])+1;if(l<= 0){l=n-i-length(w[j])-1;printf"\n%*s ",-i," ";}printf"%s ",w[j];}printf"\n";}'


# Copy UI icons
copy_icons:
	mkdir -p $(ASSETS_TARGET_PATH)/icons
	cp -aL icons/base/. $(ASSETS_TARGET_PATH)/icons
	[[ -d icons/optional ]] && cp -aL icons/optional/. $(ASSETS_TARGET_PATH)/icons || true

# Write add-on manifest
manifest:
	aab manifest -d $(DIST_TYPE)

# Build Qt forms
qt:
	aab ui

# Build ts & svelte
ts-develop:
	yarn install
	yarn run build

# Perform pre-launch steps to run add-on from source
develop: qt manifest copy_icons ts-develop

# Build add-on
build:
	aab create_dist -d $(DIST_TYPE) $(BUILD_TARGET)
	aab build_dist -d $(DIST_TYPE) $(BUILD_TARGET)
	[[ -d icons/optional ]] && cp -aL icons/optional $(DIST_ROOT_PATH)/icons/optional || true
	$(MAKE) -C $(DIST_ROOT_PATH) copy_icons
	(cd $(DIST_ROOT_PATH); yarn install; yarn run build;)
	
	aab package_dist -d $(DIST_TYPE) $(BUILD_TARGET)

.DEFAULT_GOAL: help
.PHONY: check format help build ts
