#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "arbor::units" for configuration "Release"
set_property(TARGET arbor::units APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(arbor::units PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libunits.a"
  )

list(APPEND _cmake_import_check_targets arbor::units )
list(APPEND _cmake_import_check_files_for_arbor::units "${_IMPORT_PREFIX}/lib64/libunits.a" )

# Import target "arbor::arbor" for configuration "Release"
set_property(TARGET arbor::arbor APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(arbor::arbor PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libarbor.a"
  )

list(APPEND _cmake_import_check_targets arbor::arbor )
list(APPEND _cmake_import_check_files_for_arbor::arbor "${_IMPORT_PREFIX}/lib64/libarbor.a" )

# Import target "arbor::arborenv" for configuration "Release"
set_property(TARGET arbor::arborenv APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(arbor::arborenv PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libarborenv.a"
  )

list(APPEND _cmake_import_check_targets arbor::arborenv )
list(APPEND _cmake_import_check_files_for_arbor::arborenv "${_IMPORT_PREFIX}/lib64/libarborenv.a" )

# Import target "arbor::arborio" for configuration "Release"
set_property(TARGET arbor::arborio APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(arbor::arborio PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib64/libarborio.a"
  )

list(APPEND _cmake_import_check_targets arbor::arborio )
list(APPEND _cmake_import_check_files_for_arbor::arborio "${_IMPORT_PREFIX}/lib64/libarborio.a" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
