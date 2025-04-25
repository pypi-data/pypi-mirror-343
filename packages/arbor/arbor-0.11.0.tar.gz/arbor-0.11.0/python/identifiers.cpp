#include <pybind11/pybind11.h>

#include <arbor/common_types.hpp>
#include <arbor/recipe.hpp>
#include <arbor/spike.hpp>

#include "strprintf.hpp"

namespace pyarb {

using util::pprintf;
namespace py = pybind11;

void register_identifiers(py::module& m) {
    using namespace py::literals;

    py::enum_<arb::lid_selection_policy>(m, "selection_policy",
        "Enumeration used to identify a selection policy, used by the model for selecting one of possibly multiple locations on the cell associated with a labeled item.")
        .value("round_robin", arb::lid_selection_policy::round_robin,
               "Iterate round-robin over all possible locations.")
		.value("round_robin_halt", arb::lid_selection_policy::round_robin_halt,
               "Halts at the current location until the round_robin policy is called (again).")
        .value("univalent", arb::lid_selection_policy::assert_univalent,
               "Assert that there is only one possible location associated with a labeled item on the cell. The model throws an exception if the assertion fails.");

    py::class_<arb::cell_address_type> cell_address(m, "cell_address");
    cell_address
        .def_readwrite("gid", &arb::cell_address_type::gid)
        .def_readwrite("tag", &arb::cell_address_type::tag);

    py::class_<arb::cell_local_label_type> cell_local_label_type(m, "cell_local_label",
        "For local identification of an item.\n\n"
        "cell_local_label identifies:\n"
        "(1) a labeled group of one or more items on one or more locations on the cell.\n"
        "(2) a policy for selecting one of the items.\n");

    cell_local_label_type
        .def(py::init(
            [](arb::cell_tag_type label) {
              return arb::cell_local_label_type{std::move(label)};
            }),
             "label"_a,
             "Construct a cell_local_label identifier from a label argument identifying a group of one or more items on a cell.\n"
             "The default round_robin policy is used for selecting one of possibly multiple items associated with the label.")
        .def(py::init(
            [](arb::cell_tag_type label, arb::lid_selection_policy policy) {
              return arb::cell_local_label_type{std::move(label), policy};
            }),
             "label"_a, "policy"_a,
             "Construct a cell_local_label identifier with arguments:\n"
             "  label:  The identifier of a group of one or more items on a cell.\n"
             "  policy: The policy for selecting one of possibly multiple items associated with the label.\n")
        .def(py::init([](const std::tuple<arb::cell_tag_type, arb::lid_selection_policy>& t) {
               return arb::cell_local_label_type{std::get<arb::cell_tag_type>(t), std::get<arb::lid_selection_policy>(t)};
             }),
             "Construct a cell_local_label identifier with tuple argument (label, policy):\n"
             "  label:  The identifier of a group of one or more items on a cell.\n"
             "  policy: The policy for selecting one of possibly multiple items associated with the label.\n")
        .def(py::init([](const std::pair<arb::cell_tag_type, arb::lid_selection_policy>& t) {
               return arb::cell_local_label_type{std::get<arb::cell_tag_type>(t), std::get<arb::lid_selection_policy>(t)};
             }),
             "Construct a cell_local_label identifier with tuple argument (label, policy):\n"
             "  label:  The identifier of a group of one or more items on a cell.\n"
             "  policy: The policy for selecting one of possibly multiple items associated with the label.\n")
        .def_readwrite("label",  &arb::cell_local_label_type::tag,
             "The identifier of a a group of one or more items on a cell.")
        .def_readwrite("policy", &arb::cell_local_label_type::policy,
            "The policy for selecting one of possibly multiple items associated with the label.")
        .def("__str__", [](arb::cell_local_label_type m) {return pprintf("<arbor.cell_local_label: label {}, policy {}>", m.tag, m.policy);})
        .def("__repr__",[](arb::cell_local_label_type m) {return pprintf("<arbor.cell_local_label: label {}, policy {}>", m.tag, m.policy);});

    py::implicitly_convertible<std::pair<arb::cell_tag_type, arb::lid_selection_policy>, arb::cell_local_label_type>();
    py::implicitly_convertible<std::tuple<arb::cell_tag_type, arb::lid_selection_policy>, arb::cell_local_label_type>();
    py::implicitly_convertible<py::tuple, arb::cell_local_label_type>();
    py::implicitly_convertible<arb::cell_tag_type, arb::cell_local_label_type>();

    py::class_<arb::cell_global_label_type> cell_global_label_type(m, "cell_global_label",
        "For global identification of an item.\n\n"
        "cell_global_label members:\n"
        "(1) a unique cell identified by its gid.\n"
        "(2) a cell_local_label, referring to a labeled group of items on the cell and a policy for selecting a single item out of the group.\n");

    cell_global_label_type
        .def(py::init(
            [](arb::cell_gid_type gid, arb::cell_tag_type label) {
              return arb::cell_global_label_type{gid, std::move(label)};
            }),
             "gid"_a, "label"_a,
             "Construct a cell_global_label identifier from a gid and a label argument identifying an item on the cell.\n"
             "The default round_robin policy is used for selecting one of possibly multiple items on the cell associated with the label.")
        .def(py::init(
            [](arb::cell_gid_type gid, arb::cell_local_label_type label) {
              return arb::cell_global_label_type{gid, label};
            }),
             "gid"_a, "label"_a,
             "Construct a cell_global_label identifier with arguments:\n"
             "  gid:   The global identifier of the cell.\n"
             "  label: The cell_local_label representing the label and selection policy of an item on the cell.\n")
        .def(py::init([](const std::tuple<arb::cell_gid_type, arb::cell_local_label_type>& t) {
               return arb::cell_global_label_type{std::get<arb::cell_gid_type>(t), std::get<arb::cell_local_label_type>(t)};
             }),
             "Construct a cell_global_label identifier with tuple argument (gid, label):\n"
             "  gid:   The global identifier of the cell.\n"
             "  label: The cell_local_label representing the label and selection policy of an item on the cell.\n")
        .def(py::init([](const std::tuple<arb::cell_gid_type, arb::cell_tag_type>& t) {
               return arb::cell_global_label_type{std::get<arb::cell_gid_type>(t), std::get<arb::cell_tag_type>(t)};
             }),
             "Construct a cell_global_label identifier with tuple argument (gid, label):\n"
             "  gid:   The global identifier of the cell.\n"
             "  label: The tag of an item on the cell.\n")
        .def_readwrite("gid",  &arb::cell_global_label_type::gid,
             "The global identifier of the cell.")
        .def_readwrite("label", &arb::cell_global_label_type::label,
             "The cell_local_label representing the label and selection policy of an item on the cell.")
        .def("__str__", [](arb::cell_global_label_type m) {return pprintf("<arbor.cell_global_label: gid {}, label ({}, {})>", m.gid, m.label.tag, m.label.policy);})
        .def("__repr__",[](arb::cell_global_label_type m) {return pprintf("<arbor.cell_global_label: gid {}, label ({}, {})>", m.gid, m.label.tag, m.label.policy);});


    py::implicitly_convertible<std::tuple<arb::cell_gid_type, arb::cell_local_label_type>, arb::cell_global_label_type>();
    py::implicitly_convertible<std::tuple<arb::cell_gid_type, arb::cell_tag_type>, arb::cell_global_label_type>();
    py::implicitly_convertible<py::tuple, arb::cell_global_label_type>();

    py::class_<arb::cell_remote_label_type> cell_remote_label_type(m, "cell_remote_label",
        "For remote identification of an item.\n\n"
        "cell_remote_label members:\n"
        "(1) a unique cell identified by its gid.\n"
        "(2) a cell_local_label, referring to a labeled group of items on the cell and a policy for selecting a single item out of the group.\n");

    cell_remote_label_type
        .def(py::init(
            [](arb::cell_gid_type gid, arb::cell_lid_type index) {
              return arb::cell_remote_label_type{gid, index};
            }),
             "gid"_a, "index"_a,
             "Construct a cell_remote_label identifier from a gid and an index identifying an item on the cell.\n"
             "The default round_robin policy is used for selecting one of possibly multiple items on the cell associated with the label.")
        .def(py::init(
            [](arb::cell_gid_type gid, arb::cell_lid_type index) {
              return arb::cell_remote_label_type{gid, index};
            }),
             "gid"_a, "label"_a,
             "Construct a cell_remote_label identifier with arguments:\n"
             "  gid:   The remote identifier of the cell.\n"
             "  index: An index uniquely addressing an item on the remote cell.\n")
        .def(py::init([](const std::tuple<arb::cell_gid_type, arb::cell_lid_type>& t) { return arb::cell_remote_label_type{std::get<0>(t), std::get<1>(t)}; }),
             "Construct a cell_remote_label identifier with tuple argument (gid, index):\n"
             "  gid:   The remote identifier of the cell.\n"
             "  index: An index uniquely addressing an item on the remote cell.\n")
        .def_readwrite("gid",  &arb::cell_remote_label_type::rid, "The remote identifier of the cell.")
        .def_readwrite("index", &arb::cell_remote_label_type::index, "  An index uniquely addressing an item on the remote cell.")
        .def("__str__", [](arb::cell_remote_label_type m) {return pprintf("<arbor.cell_remote_label: gid {}, index {}>", m.rid, m.index);})
        .def("__repr__",[](arb::cell_remote_label_type m) {return pprintf("<arbor.cell_remote_label: gid {}, index {}>", m.rid, m.index);});


    py::implicitly_convertible<std::tuple<arb::cell_gid_type, arb::cell_lid_type>, arb::cell_remote_label_type>();
    py::implicitly_convertible<py::tuple, arb::cell_remote_label_type>();

    py::class_<arb::cell_member_type> cell_member(m, "cell_member",
        "For global identification of a cell-local item.\n\n"
        "Items of cell_member must:\n"
        "  (1) be associated with a unique cell, identified by the member gid;\n"
        "  (2) identify an item within a cell-local collection by the member index.\n");

    cell_member
        .def(py::init(
            [](arb::cell_gid_type gid, arb::cell_lid_type idx) {
                return arb::cell_member_type{gid, idx};
            }),
            "gid"_a, "index"_a,
            "Construct a cell member identifier with arguments:\n"
            "  gid:     The global identifier of the cell.\n"
            "  index:   The cell-local index of the item.\n")
        .def(py::init([](py::tuple t) {
                if (py::len(t)!=2) throw std::runtime_error("tuple length != 2");
                return arb::cell_member_type{t[0].cast<arb::cell_gid_type>(), t[1].cast<arb::cell_lid_type>()};
            }),
            "Construct a cell member identifier with tuple argument (gid, index):\n"
            "  gid:     The global identifier of the cell.\n"
            "  index:   The cell-local index of the item.\n")
        .def_readwrite("gid",   &arb::cell_member_type::gid,
            "The global identifier of the cell.")
        .def_readwrite("index", &arb::cell_member_type::index,
            "Cell-local index of the item.")
        .def("__str__", [](arb::cell_member_type m) {return pprintf("<arbor.cell_member: gid {}, index {}>", m.gid, m.index);})
        .def("__repr__",[](arb::cell_member_type m) {return pprintf("<arbor.cell_member: gid {}, index {}>", m.gid, m.index);});

    py::implicitly_convertible<py::tuple, arb::cell_member_type>();

    py::enum_<arb::cell_kind>(m, "cell_kind",
        "Enumeration used to identify the cell kind, used by the model to group equal kinds in the same cell group.")
        .value("benchmark", arb::cell_kind::benchmark,
            "Proxy cell used for benchmarking.")
        .value("cable", arb::cell_kind::cable,
            "A cell with morphology described by branching 1D cable segments.")
        .value("lif", arb::cell_kind::lif,
            "Leaky-integrate and fire neuron.")
        .value("spike_source", arb::cell_kind::spike_source,
            "Proxy cell that generates spikes from a spike sequence provided by the user.");

    py::enum_<arb::backend_kind>(m, "backend",
        "Enumeration used to indicate which hardware backend to execute a cell group on.")
        .value("gpu", arb::backend_kind::gpu,
            "Use GPU backend.")
        .value("multicore", arb::backend_kind::multicore,
            "Use multicore backend.");

    // Probes
    py::class_<arb::probe_info> probe(m, "probe");
    probe
        .def("__repr__", [](const arb::probe_info& p){return util::pprintf("<arbor.probe: tag {}>", p.tag);})
        .def("__str__",  [](const arb::probe_info& p){return util::pprintf("<arbor.probe: tag {}>", p.tag);});

    py::class_<arb::spike> spike(m, "spike");
    spike
        .def(py::init([](const arb::cell_member_type& m, arb::time_type t) -> arb::spike { return {m, t}; }))
        .def_readwrite("source", &arb::spike::source, "The global identifier of the cell.")
        .def_readwrite("time", &arb::spike::time, "The time of spike.")
        .def("__repr__", [](const arb::spike& s){return util::pprintf("<arbor.spike: {}>", s);})
        .def("__str__",  [](const arb::spike& s){return util::pprintf("<arbor.spike: {}>", s);});

}

} // namespace pyarb
