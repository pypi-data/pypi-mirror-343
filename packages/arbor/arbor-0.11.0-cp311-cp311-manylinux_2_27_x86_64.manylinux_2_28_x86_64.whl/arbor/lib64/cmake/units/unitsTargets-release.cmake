#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "units::units" for configuration "Release"
set_property(TARGET units::units APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(units::units PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libunits.a"
  )

list(APPEND _cmake_import_check_targets units::units )
list(APPEND _cmake_import_check_files_for_units::units "${_IMPORT_PREFIX}/lib64/libunits.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
