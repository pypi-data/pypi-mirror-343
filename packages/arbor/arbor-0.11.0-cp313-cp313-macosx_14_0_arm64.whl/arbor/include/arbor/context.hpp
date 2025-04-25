#pragma once

#include <memory>

#include <arbor/export.hpp>

namespace arb {

constexpr static int gpu_nil_id = -1;

// Requested dry-run parameters.
struct dry_run_info {
    unsigned num_ranks;
    unsigned num_cells_per_rank;
    dry_run_info(unsigned ranks, unsigned cells_per_rank):
            num_ranks(ranks),
            num_cells_per_rank(cells_per_rank) {}
};

// A description of local computation resources to use in a computation.
// By default, a proc_allocation will comprise one thread and no GPU.

struct proc_allocation {
    unsigned long num_threads = 1;

    // The gpu id corresponds to the `int device` parameter used by
    // CUDA/HIP API calls to identify gpu devices.
    // A gpud id of gpu_nil_id indicates no GPU device is to be used.
    // See documenation for cuda[/hip]SetDevice and cuda[/hip]DeviceGetAttribute.
    int gpu_id = gpu_nil_id;

    // Try to use HWLOC to bind threads/procs.
    bool bind_procs = false;
    bool bind_threads = false;

    proc_allocation() = default;

    proc_allocation(unsigned long threads, int gpu, bool bind_proc=false, bool bind_thread=false):
        num_threads(threads),
        gpu_id(gpu),
        bind_procs(bind_proc),
        bind_threads(bind_thread)
    {}

    bool has_gpu() const {
        return gpu_id>=0;
    }
};

// arb::execution_context encapsulates the execution resources used in
// a simulation, namely the task system thread pools, GPU handle, and
// MPI communicator if applicable.

// Forward declare execution_context.
struct execution_context;

// arb::context is an opaque handle for the execution context for use
// in the public API, implemented as a shared pointer.
using context = std::shared_ptr<execution_context>;

// To connect to external simulations
template<typename Comm>
ARB_ARBOR_API void make_remote_connection(context, Comm);

// Helpers for creating contexts. These are implemented in the back end.

// Non-distributed context using the requested resources.
ARB_ARBOR_API context make_context(const proc_allocation& resources = proc_allocation{});

// Distributed context that uses MPI communicator comm, and local resources
// described by resources. Or dry run context that uses dry_run_info.
template <typename Comm>
ARB_ARBOR_API context make_context(const proc_allocation& resources, Comm comm);

template <typename Comm>
ARB_ARBOR_API context make_context(const proc_allocation& resources, Comm comm, Comm remote);

// Queries for properties of execution resources in a context.

ARB_ARBOR_API std::string distribution_type(context);
ARB_ARBOR_API bool has_gpu(context);
ARB_ARBOR_API unsigned num_threads(context);
ARB_ARBOR_API bool has_mpi(context);
ARB_ARBOR_API unsigned num_ranks(context);
ARB_ARBOR_API unsigned rank(context);

}
