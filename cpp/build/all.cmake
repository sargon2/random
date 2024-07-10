# This bootstrap-vcpkg.sh call is only needed so the vcpkg binary is in place for the update-baseline call.
if(UNIX)
    execute_process(COMMAND ./vcpkg/bootstrap-vcpkg.sh COMMAND_ERROR_IS_FATAL ANY)
elseif(WIN32)
    execute_process(COMMAND vcpkg\\bootstrap-vcpkg.bat COMMAND_ERROR_IS_FATAL ANY)
endif()

# The builtin-baseline is stored in vcpkg.json and shouldn't be, since the version is already
# pinned by the submodule pointer.  So to make it as transparent as possible, we update the baseline here,
# which will unfortunately cause the file to show as modified in git, but that modification should be
# committed when present.
#
# TODO store the vcpkg.json file without the baseline, then update it with "--add-initial-baseline" each time.
# To do this we have to copy the vcpkg.json to a subfolder and run the build there, so it doesn't update the actual vcpkg.json.
if(UNIX)
    execute_process(COMMAND ./vcpkg/vcpkg x-update-baseline COMMAND_ERROR_IS_FATAL ANY)
elseif(WIN32)
    execute_process(COMMAND vcpkg\\vcpkg.exe x-update-baseline COMMAND_ERROR_IS_FATAL ANY)
endif()

file(MAKE_DIRECTORY build-output)
execute_process(COMMAND cmake --preset default .. WORKING_DIRECTORY build-output COMMAND_ERROR_IS_FATAL ANY)
execute_process(COMMAND cmake --build . WORKING_DIRECTORY build-output COMMAND_ERROR_IS_FATAL ANY)
