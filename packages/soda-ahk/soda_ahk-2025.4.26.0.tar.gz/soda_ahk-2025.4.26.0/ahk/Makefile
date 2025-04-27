all: build

.PHONY: build

build:
	cmake --preset windows
	cmake --build build
	gen_lsp_tdm

clean:
	pwsh -nop -c "rm -r -Force build"

zigbuild:
	zig cc toggle_icons.c -o ../ahk_resources/toggle-icons.exe
