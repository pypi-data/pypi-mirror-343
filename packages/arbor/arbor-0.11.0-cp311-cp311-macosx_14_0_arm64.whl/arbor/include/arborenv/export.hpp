#pragma once

//#ifndef ARB_EXPORT_DEBUG
//#   define ARB_EXPORT_DEBUG
//#endif

#include <arbor/util/visibility.hpp>

/* library build type (ARB_ARBORENV_STATIC_LIBRARY/ARB_ARBORENV_SHARED_LIBRARY) */
#define ARB_ARBORENV_STATIC_LIBRARY

#ifndef ARB_ARBORENV_EXPORTS
#   if defined(arborenv_EXPORTS)
        /* we are building arborenv dynamically */
#       ifdef ARB_EXPORT_DEBUG
#           pragma message "we are building arborenv dynamically"
#       endif
#       define ARB_ARBORENV_API ARB_SYMBOL_EXPORT
#   elif defined(arborenv_EXPORTS_STATIC)
        /* we are building arborenv statically */
#       ifdef ARB_EXPORT_DEBUG
#           pragma message "we are building arborenv statically"
#       endif
#       define ARB_ARBORENV_API
#   else
        /* we are using the library arborenv */
#       if defined(ARB_ARBORENV_SHARED_LIBRARY)
            /* we are importing arborenv dynamically */
#           ifdef ARB_EXPORT_DEBUG
#              pragma message "we are importing arborenv dynamically"
#           endif
#           define ARB_ARBORENV_API ARB_SYMBOL_IMPORT
#       else
            /* we are importing arborenv statically */
#           ifdef ARB_EXPORT_DEBUG
#               pragma message "we are importing arborenv statically"
#           endif
#           define ARB_ARBORENV_API
#       endif
#   endif
#endif
