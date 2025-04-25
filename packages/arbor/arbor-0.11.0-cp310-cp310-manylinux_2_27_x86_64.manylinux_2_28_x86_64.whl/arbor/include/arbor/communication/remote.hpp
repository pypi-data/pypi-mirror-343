#pragma once

#include <cstring>
#include <cstdint>
#include <stdexcept>
#include <variant>
#include <vector>
#include <string>

#include <mpi.h>

/* Remote Support Tooling for Arbor CoSimulation
**
** This is a stand-alone header to facilitate coupling Arbor to an external
** simulator. The exchange protocol is based on spike data, see below for the
** definition of the spike type, and an in-band control block. The latter is
** handled using the `msg_*` types below.
**
** We package the spike and control message exchanges into two main methods
**
** 1. exchange_ctrl
** 2. gather_spikes
**
** for more details see the Arbor documentation on interconnectivity and the
** developer's documentation on spike exchange in general. See also the `remote`
** example for a more practical introduction.
**
** This is distributed as part of Arbor and under its license.
 */

namespace arb {
namespace remote {

// Magic protocol tag
constexpr std::uint8_t ARB_REMOTE_MAGIC = 0xAB;

// Remote protocol version
constexpr std::uint8_t ARB_REMOTE_VERSION_MAJOR = 0x00;
constexpr std::uint8_t ARB_REMOTE_VERSION_MINOR = 0x01;
constexpr std::uint8_t ARB_REMOTE_VERSION_PATCH = 0x00;

// Message buffer length
constexpr std::size_t ARB_REMOTE_MESSAGE_LENGTH = 1024;
 // Buffer size consumed by header:
 // 1B Magic
 // 3B Version
 // 1B Message kind
constexpr std::size_t ARB_REMOTE_HEADER_LENGTH  = 1 + 3 + 1;

// Who sends the control message?
constexpr int ARB_REMOTE_ROOT = 0;

// Messages
// Null message, nothing to say. Potentially retry exchange.
struct msg_null {
    static constexpr std::uint8_t tag = 0x00;
    std::uint8_t null = 0x0;
};

// Encountered an unrecoverable yet non-fatal error. Will
// terminate after sending this. Reason is included.
struct msg_abort {
    static constexpr std::uint8_t tag = 0x01;
    char reason[512];
};

// Ready to begin next epoch in simulation period.
struct msg_epoch {
    static constexpr std::uint8_t tag = 0x02;
    double t_start;
    double t_end;
};

// Reached end of simulation period.
struct msg_done {
    static constexpr std::uint8_t tag = 0x03;
    float time = 0.0f;
};

// Union of all message types.
using ctrl_message = std::variant<msg_null,
                                  msg_abort,
                                  msg_epoch,
                                  msg_done>;

// Exceptions
// Base class
struct remote_error: std::runtime_error {
    remote_error(const std::string& msg): std::runtime_error{msg} {}
};

// Protocal meta data check failed. Are we using correct version of this header+Arbor?
struct unexpected_version: remote_error {
    unexpected_version(): remote_error{"Arbor remote: Magic or Version mismatch."} {}
};

// Message had a tag we do not know. Either the protocol is messed up or the message got
// corrupted.
struct unexpected_message: remote_error {
    unexpected_message(): remote_error{"Arbor remote: Received unknown tag."} {}
};

// Message had a tag we do not know. Either the protocol is messed up or the message got
// corrupted.
struct illegal_communicator: remote_error {
    illegal_communicator(): remote_error{"Arbor remote: Intercommunicator required."} {}
};


// One of the underlying MPI routines bailed.
struct mpi_error: remote_error {
    mpi_error(const std::string& where, const std::string& what):
        remote_error{"MPI failed in " + where + " with error: " + what} {}
};

inline
void mpi_checked(int rc, const std::string& where) {
    if (rc != MPI_SUCCESS) {
        char str[MPI_MAX_ERROR_STRING] = {0};
        if (int len=0; MPI_Error_string(rc, str, &len) != MPI_SUCCESS) {
            throw mpi_error{where, "unknown MPI error"};
        }
        throw mpi_error{where, str};
    }
}

// Exchange control message. NOTE: This makes clever (?) use of MPI_Allreduce
// to achieve simulatenous duplex mode broadcast by preparing zeroed buffers
// on all ranks except the root and then adding up tons of zeros with a single
// payload.
inline
ctrl_message exchange_ctrl(const ctrl_message& msg, MPI_Comm comm) {
    static_assert(sizeof(ctrl_message) + ARB_REMOTE_HEADER_LENGTH <= ARB_REMOTE_MESSAGE_LENGTH, "Message payload is too large to send. Please adjust ARB_REMOTE_MESSAGE_LENGTH.");
    int is_inter = 0;
    mpi_checked(MPI_Comm_test_inter(comm, &is_inter), "exchange ctrl block: comm type");
    if (!is_inter) throw illegal_communicator{};
    int rank = -1;
    mpi_checked(MPI_Comm_rank(comm, &rank), "exchange ctrl block: comm rank");
    std::vector<char> send(ARB_REMOTE_MESSAGE_LENGTH, 0x0);
    std::vector<char> recv(ARB_REMOTE_MESSAGE_LENGTH, 0x0);
    // Prepare byte buffer for sending.
    if (rank == ARB_REMOTE_ROOT) {
        std::size_t ptr = 0;
        send[ptr++] = ARB_REMOTE_MAGIC;
        send[ptr++] = ARB_REMOTE_VERSION_MAJOR;
        send[ptr++] = ARB_REMOTE_VERSION_MINOR;
        send[ptr++] = ARB_REMOTE_VERSION_PATCH;
        auto visitor = [&send, &ptr] (auto&& m) {
            using T = std::decay_t<decltype(m)>;
            send[ptr++] = T::tag;
            std::memcpy(send.data() + ptr, &m, sizeof(m));
        };
        std::visit(visitor, msg);
    }
    mpi_checked(MPI_Allreduce((const void*) send.data(),
                              (void*)       recv.data(),
                              ARB_REMOTE_MESSAGE_LENGTH, MPI_CHAR,
                              MPI_SUM,
                              comm),
                "exchange control block: Allreduce");
    std::size_t ptr = 0;
    std::uint8_t mag = recv[ptr++];
    std::uint8_t maj = recv[ptr++];
    std::uint8_t min = recv[ptr++];
    std::uint8_t pat = recv[ptr++];
    if ((mag != ARB_REMOTE_MAGIC) ||
        (maj != ARB_REMOTE_VERSION_MAJOR) ||
        (min != ARB_REMOTE_VERSION_MINOR) ||
        (pat != ARB_REMOTE_VERSION_PATCH)) throw unexpected_message{};
    std::uint8_t tag = recv[ptr++];
    auto payload = recv.data() + ptr;
    switch(tag) {
        case msg_null::tag: {
            msg_null result;
            std::memcpy(&result, payload, sizeof(result));
            return result;
        }
        case msg_abort::tag: {
            msg_abort result;
            std::memcpy(&result, payload, sizeof(result));
            return result;
        }
        case msg_epoch::tag: {
            msg_epoch result;
            std::memcpy(&result, payload, sizeof(result));
            return result;
        }
        case msg_done::tag: {
            msg_done result;
            std::memcpy(&result, payload, sizeof(result));
            return result;
        }
        default: throw unexpected_message{};
    }
}

// Replicate some types from Arbor so this becomes a stand-alone header.
using arb_time_type = double;
using arb_lid_type  = std::uint32_t;
using arb_gid_type  = std::uint32_t;

struct arb_cell_id {
    arb_gid_type gid;
    arb_lid_type lid;
};

struct arb_spike {
    arb_cell_id source;
    arb_time_type time;
};

inline
std::vector<arb_spike> gather_spikes(const std::vector<arb_spike>& send, MPI_Comm comm) {
    // Setup and sanity check
    int is_inter = 0;
    mpi_checked(MPI_Comm_test_inter(comm, &is_inter), "gather spikes: comm type");
    if (!is_inter) throw illegal_communicator{};
    int size = -1;
    mpi_checked(MPI_Comm_size(comm, &size), "gather spikes: comm size");
    // Get the number of spikes per rank
    int send_count = send.size();
    std::vector<int> counts(size, 0);
    mpi_checked(MPI_Allgather(&send_count, 1, MPI_INT, counts.data(), 1, MPI_INT, comm),
                "gather spikes: exchanging counts");
    // Prepare offset buffer (displ) and scale by sizes in bytes.
    int recv_bytes = 0;
    int recv_count = 0;
    std::vector<int> displs(size, 0);
    for (int ix = 0; ix < size; ++ix) {
        recv_count += counts[ix];         // Number of items to receive.
        counts[ix] *= sizeof(arb_spike);  // Number of Bytes for rank ``ix`
        displs[ix]  = recv_bytes;         // Offset for rank `ix` in Bytes
        recv_bytes += counts[ix];         // Total number of items so far

    }
    // Transfer spikes.
    std::vector<arb_spike> recv(recv_count);
    mpi_checked(MPI_Allgatherv(send.data(), send_count*sizeof(arb_spike), MPI_BYTE, // send buffer
                               recv.data(), counts.data(), displs.data(), MPI_BYTE, // recv buffer
                               comm),
                "gather spikes: exchanging payload");
    return recv;
}

} // remote
} // arb
