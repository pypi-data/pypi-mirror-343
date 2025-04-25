#pragma once

#include <arbor/export.hpp>

namespace arb {
ARB_ARBOR_API extern const char* source_id;
ARB_ARBOR_API extern const char* arch;
ARB_ARBOR_API extern const char* build_config;
ARB_ARBOR_API extern const char* version;
ARB_ARBOR_API extern const char* full_build_id;
constexpr int version_major = 0;
constexpr int version_minor = 11;
constexpr int version_patch = 0;
ARB_ARBOR_API extern const char* version_dev;
}

#define ARB_SOURCE_ID "unknown commit"
#define ARB_ARCH "native"
#define ARB_BUILD_CONFIG "RELEASE"
#define ARB_FULL_BUILD_ID "source_id=unknown commit;version=0.11.0;arch=native;config=RELEASE;NEUROML_ENABLED;"
#define ARB_VERSION "0.11.0"
#define ARB_VERSION_MAJOR 0
#define ARB_VERSION_MINOR 11
#define ARB_VERSION_PATCH 0
#ifndef ARB_NEUROML_ENABLED
#define ARB_NEUROML_ENABLED
#endif
