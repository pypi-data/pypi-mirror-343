#pragma once

//#ifndef ARB_EXPORT_DEBUG
//#   define ARB_EXPORT_DEBUG
//#endif

#include <arbor/util/visibility.hpp>

/* library build type (ARB_ARBOR_STATIC_LIBRARY/ARB_ARBOR_SHARED_LIBRARY) */
#define ARB_ARBOR_STATIC_LIBRARY

#ifndef ARB_ARBOR_EXPORTS
#   if defined(arbor_EXPORTS)
        /* we are building arbor dynamically */
#       ifdef ARB_EXPORT_DEBUG
#           pragma message "we are building arbor dynamically"
#       endif
#       define ARB_ARBOR_API ARB_SYMBOL_EXPORT
#   elif defined(arbor_EXPORTS_STATIC)
        /* we are building arbor statically */
#       ifdef ARB_EXPORT_DEBUG
#           pragma message "we are building arbor statically"
#       endif
#       define ARB_ARBOR_API
#   else
        /* we are using the library arbor */
#       if defined(ARB_ARBOR_SHARED_LIBRARY)
            /* we are importing arbor dynamically */
#           ifdef ARB_EXPORT_DEBUG
#              pragma message "we are importing arbor dynamically"
#           endif
#           define ARB_ARBOR_API ARB_SYMBOL_IMPORT
#       else
            /* we are importing arbor statically */
#           ifdef ARB_EXPORT_DEBUG
#               pragma message "we are importing arbor statically"
#           endif
#           define ARB_ARBOR_API
#       endif
#   endif
#endif
