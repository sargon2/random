@echo off
setlocal enabledelayedexpansion

set cmake_command=cmake

if "%1"=="" (
    set cmake_command=!cmake_command! -P build/all.cmake
) else (
    :loop
    if "%~1"=="" goto done
    set cmake_command=!cmake_command! -P build/%~1.cmake
    shift
    goto loop
)

:done
%cmake_command%
