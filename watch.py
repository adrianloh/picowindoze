import os
import re
import hashlib
import shutil
from time import sleep
import os
import subprocess

CMAKELIST = """
cmake_minimum_required(VERSION 3.12)

# Pull in Pico SDK (must be before project)
include(pico_sdk_import.cmake)

project(picoblink)

# Initialize the Pico SDK
pico_sdk_init()

# Create the executable for the project
add_executable(picoblink 
    ##FILES##
)

# Add any additional libraries you want to link against
target_link_libraries(picoblink 
    ##LIBS##
)

# Create map/bin/hex/uf2 files
pico_add_extra_outputs(picoblink)

# Enable stdout on USB and UART
pico_enable_stdio_usb(picoblink 1)
pico_enable_stdio_uart(picoblink 1)
"""


class File:
    def __init__(self, checksum, includes):
        self.checksum = checksum
        self.includes = includes


def scan_files(directory):
    files = {}
    for filename in os.listdir(directory):
        if filename.endswith(".c") or filename.endswith(".cpp") or filename.endswith(".h"):
            lines = open(filename).readlines()
            string_lines = "".join(lines)
            md5_hash = hashlib.md5(string_lines.encode('utf-8')).hexdigest()
            includes = get_includes(lines)
            files[filename] = File(md5_hash, includes)
    return files


def get_includes(lines):
    """
    Takes a list of lines and returns a list of all the includes in that file
    formatted for CMakeLists.txt e.g.
    #include "hardware/gpio.h" -> hardware_gpio
    """
    re_include = re.compile(r'#include ["<](\w+)/(\w+).h[">]')
    include_matches = [re.match(re_include, l) for l in lines if re_include.match(l)]
    includes = []
    for match in include_matches:
        includes.append(f"{match.group(1)}_{match.group(2)}")
    return includes


if __name__ == "__main__":

    last_files = {}

    while True:

        files = scan_files(".")
        changed_files = []

        for fn, file in files.items():
            if fn not in last_files:
                print(f"New file: {fn}")
                changed_files.append(fn)
            elif file.checksum != last_files[fn].checksum:
                print(f"File changed: {fn}")
                changed_files.append(fn)
            else:
                pass

        if len(changed_files) == 0:
            sleep(2)
            continue

        last_files = files
        project_name = os.path.basename(os.getcwd())

        # Print out the files that have changed
        for fn, file in files.items():
            print(f"{fn} includes: {file.includes} and checksum: {file.checksum}")

        print("\nWriting CMakeLists.txt and running `cmake`\n")

        # Write the CMakeLists.txt file        
        cmake_file = CMAKELIST.replace("##FILES##", "\n    ".join(files.keys()))
        libs = set()
        for fn, file in files.items():
            libs.update(file.includes)
        cmake_file = cmake_file.replace("##LIBS##", "\n    ".join(libs))
        cmake_file = cmake_file.replace("picoblink", project_name)
        open("CMakeLists.txt", "w").write(cmake_file)

        # Run cmake
        shutil.rmtree("build", ignore_errors=True)
        ok = os.system("cmake -G Ninja -B build .")
        if ok != 0:
            print("\n######\ncmake failed\n######\n")
            continue
        
        # Run ninja
        print("\nRunning ninja\n")
        #os.chdir("build")
        proc = subprocess.run("ninja -C build -j 16", shell=True, capture_output=True)
        if proc.returncode != 0 or proc.stdout.decode("utf-8").find("warning") != -1:
            print(proc.stdout.decode("utf-8"))
            print("\n######\nninja failed\n######\n")
            continue
        if not os.path.exists(f"build/{project_name}.elf"):
            print(f"\n######\nBinary not found {project_name}.elf\n######\n")
            continue

        # Copy the elf file to the openocd directory and upload to the Pico
        print("\nUploading firmware\n")
        shutil.copy(f"build/{project_name}.elf", f"openocd/{project_name}.elf")
        os.chdir("openocd")
        ok = os.system(f"""openocd -f cmsis-dap.cfg -f rp2040.cfg -c "adapter speed 5000" -c "program {project_name}.elf verify reset exit" """)
        os.chdir("..")
        if ok != 0:
            print("\n######\nUpload failed\n######\n")
            continue

        print("\nUploaded firmware. Watching for changes...\n\n\n")