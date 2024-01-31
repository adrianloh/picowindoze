cmake_minimum_required(VERSION 3.12)

# Pull in Pico SDK (must be before project)
# set(PICO_SDK_PATH "C:/Users/TTWP/Desktop/pico-sdk")
include(pico_sdk_import.cmake)

project(picoblink)

# Initialize the Pico SDK
pico_sdk_init()

# Create the executable for the project
add_executable(picoblink 
    main.c
)

# Add any additional libraries you want to link against
target_link_libraries(picoblink 
    pico_stdlib
)

# Create map/bin/hex/uf2 files
pico_add_extra_outputs(picoblink)

# If you want to auto-set the USB as serial COM port
pico_enable_stdio_usb(picoblink 1)
pico_enable_stdio_uart(picoblink 0)
