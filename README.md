# Compiling for Pico on Windows

The easiest is to download this:

```
https://github.com/raspberrypi/pico-setup-windows/blob/master/docs/tutorial.md
```

## Setup

1. Set the environment variable `PICO_SDK_PATH` and point it to the root of the Pico SDK.

2. `cmake` looks for `CMakeLists.txt` to start the build process. It includes `pico_sdk_import.cmake` (from the SDK) which pulls in the relevant files from the Pico SDK.

We run `cmake` with with these paramaters:

```
cmake -G Ninja -B build .
```

This tells `cmake` to generate build files for `ninja`. By default it will generate `make` build files e.g `-G "NMake Makefiles"`

`-B` tells it to dump all the build files into the `build` subfolder.

Inside `build` we finally run:

```
ninja -j 16
```

It we're using `make`, then it would be:

```
make -j 16
```

The `-j` sets how many threads to use.

Essentially all this cross-compile mumbo jumbo boils down to 3 files:

1. The compiler, from the [GNU ARM Embedded Toolchian](https://developer.arm.com/downloads/-/gnu-rm) which then gives you the "cross platform" `gcc`:
```
arm-none-eabi-g++.exe
arm-none-eabi-gcc.exe
```

2. `cmake`` -- download: https://cmake.org/download/

3. `ninja`` -- precompiled: https://github.com/ninja-build/ninja

Or using `apt`:

```
sudo apt install ninja-build
```