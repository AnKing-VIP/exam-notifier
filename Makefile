SHELL = /bin/bash

PACKAGE_NAME=exam_notifier
ASSETS_TARGET_PATH = build/dist/src/$(PACKAGE_NAME)/assets

SOURCE_FOLDER = src/
TEST_FLAGS ?= -n4
DIST_TYPE ?= local
BUILD_TARGET ?= current

# Run code checkers
check:
	python -m mypy $(SOURCE_FOLDER)
	python -m flake8 $(SOURCE_FOLDER)

# Run code formatters
format:
	python -m isort --recursive $(SOURCE_FOLDER)
	python -m black $(SOURCE_FOLDER)

# Show help message
help:
	@echo "$$(tput bold)Available targets:$$(tput sgr0)";echo;sed -ne"/^# /{h;s/.*//;:d" -e"H;n;s/^# //;td" -e"s/:.*//;G;s/\\n# /---/;s/\\n/ /g;p;}" ${MAKEFILE_LIST}|LC_ALL='C' sort -f|awk -F --- -v n=$$(tput cols) -v i=19 -v a="$$(tput setaf 6)" -v z="$$(tput sgr0)" '{printf"%s%*s%s ",a,-i,$$1,z;m=split($$2,w," ");l=n-i;for(j=1;j<=m;j++){l-=length(w[j])+1;if(l<= 0){l=n-i-length(w[j])-1;printf"\n%*s ",-i," ";}printf"%s ",w[j];}printf"\n";}'


# Perform pre-launch steps to run add-on from source
develop:
	mkdir -p src/$(PACKAGE_NAME)/assets/icons
	cp -aL icons/base/. src/$(PACKAGE_NAME)/assets/icons
	[[ -d icons/optional ]] && cp -aL icons/optional/. src/$(PACKAGE_NAME)/assets/icons

# Build add-on
build:
	aab create_dist -d $(DIST_TYPE) $(BUILD_TARGET)
	aab build_dist -d $(DIST_TYPE) $(BUILD_TARGET)
	# Copy assets
	mkdir -p $(ASSETS_TARGET_PATH)
	mkdir -p $(ASSETS_TARGET_PATH)/icons
	cp -aL icons/base/. $(ASSETS_TARGET_PATH)/icons
	[[ -d icons/optional ]] && cp -aL icons/optional/. $(ASSETS_TARGET_PATH)/icons
	aab package_dist -d $(DIST_TYPE) $(BUILD_TARGET)

.DEFAULT_GOAL: help
.PHONY: check format help build
