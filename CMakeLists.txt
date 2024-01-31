
cmake_minimum_required(VERSION 3.12)

# Pull in Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(picowindoze)

# Initialize the Pico SDK
pico_sdk_init()

# Create the executable for the project
add_executable(picowindoze 
    main.c
)

# Add any additional libraries you want to link against
target_link_libraries(picowindoze 
    pico_time
    pico_stdlib
)

# Create map/bin/hex/uf2 files
pico_add_extra_outputs(picowindoze)

# Enable stdout on USB and UART
pico_enable_stdio_usb(picowindoze 1)
pico_enable_stdio_uart(picowindoze 1)
