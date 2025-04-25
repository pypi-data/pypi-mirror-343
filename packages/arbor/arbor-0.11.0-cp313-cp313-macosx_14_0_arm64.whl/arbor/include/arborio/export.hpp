#pragma once

//#ifndef ARB_EXPORT_DEBUG
//#   define ARB_EXPORT_DEBUG
//#endif

#include <arbor/util/visibility.hpp>

/* library build type (ARB_ARBORIO_STATIC_LIBRARY/ARB_ARBORIO_SHARED_LIBRARY) */
#define ARB_ARBORIO_STATIC_LIBRARY

#ifndef ARB_ARBORIO_EXPORTS
#   if defined(arborio_EXPORTS)
        /* we are building arborio dynamically */
#       ifdef ARB_EXPORT_DEBUG
#           pragma message "we are building arborio dynamically"
#       endif
#       define ARB_ARBORIO_API ARB_SYMBOL_EXPORT
#   elif defined(arborio_EXPORTS_STATIC)
        /* we are building arborio statically */
#       ifdef ARB_EXPORT_DEBUG
#           pragma message "we are building arborio statically"
#       endif
#       define ARB_ARBORIO_API
#   else
        /* we are using the library arborio */
#       if defined(ARB_ARBORIO_SHARED_LIBRARY)
            /* we are importing arborio dynamically */
#           ifdef ARB_EXPORT_DEBUG
#              pragma message "we are importing arborio dynamically"
#           endif
#           define ARB_ARBORIO_API ARB_SYMBOL_IMPORT
#       else
            /* we are importing arborio statically */
#           ifdef ARB_EXPORT_DEBUG
#               pragma message "we are importing arborio statically"
#           endif
#           define ARB_ARBORIO_API
#       endif
#   endif
#endif
