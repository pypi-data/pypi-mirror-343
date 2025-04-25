#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include <pybind11/pybind11.h>
#include <pybind11/pytypes.h>
#include <pybind11/stl.h>

#include <arbor/network.hpp>
#include <arbor/network_generation.hpp>
#include <arbor/util/any_visitor.hpp>
#include <arborio/label_parse.hpp>
#include <arborio/networkio.hpp>

#include <string>
#include <unordered_map>
#include <variant>

#include "error.hpp"
#include "strprintf.hpp"

namespace py = pybind11;

namespace pyarb {

void register_network(py::module& m) {
    using namespace py::literals;
    // types
    py::class_<arb::network_site_info> network_site_info(m, "network_site_info", "Identifies a network site to connect to / from");
    py::class_<arb::network_connection_info> network_connection_info(m, "network_connection_info", "Identifies a network connection");
    py::class_<arb::network_selection> network_selection(m, "network_selection", "Network selection.");
    py::class_<arb::network_value> network_value(m, "network_value", "Network value.");
    py::class_<arb::network_description> network_description(m, "network_description", "Network description.");

    network_site_info
        .def_readwrite("gid", &arb::network_site_info::gid)
        .def_readwrite("kind", &arb::network_site_info::kind)
        .def_readwrite("label", &arb::network_site_info::label)
        .def_readwrite("location", &arb::network_site_info::location)
        .def_readwrite("global_location", &arb::network_site_info::global_location)
        .def("__repr__", [](const arb::network_site_info& s) { return util::pprintf("{}", s); })
        .def("__str__", [](const arb::network_site_info& s) { return util::pprintf("{}", s); });

    network_connection_info
        .def_readwrite("source", &arb::network_connection_info::source)
        .def_readwrite("target", &arb::network_connection_info::target)
        .def_readwrite("weight", &arb::network_connection_info::weight)
        .def_readwrite("delay", &arb::network_connection_info::delay)
        .def("__repr__", [](const arb::network_connection_info& c) { return util::pprintf("{}", c); })
        .def("__str__", [](const arb::network_connection_info& c) { return util::pprintf("{}", c); });

    network_selection
        .def_static("custom",
                    [](arb::network_selection::custom_func_type func) {
                        return arb::network_selection::custom([=](const arb::network_site_info& source, const arb::network_site_info& target) {
                            return try_catch_pyexception(
                                [&]() {
                                    pybind11::gil_scoped_acquire guard;
                                    return func(source, target);
                                },
                                "Python error already thrown");
                        });
                    })
        .def("__str__", [](const arb::network_selection& s) { return util::pprintf("<arbor.network_selection: {}>", s); })
        .def("__repr__", [](const arb::network_selection& s) { return util::pprintf("{}", s); });

    network_value
        .def_static("custom",
                    [](arb::network_value::custom_func_type func) {
                        return arb::network_value::custom([=](const arb::network_site_info& source, const arb::network_site_info& target) {
                            return try_catch_pyexception(
                                [&]() {
                                    pybind11::gil_scoped_acquire guard;
                                    return func(source, target);
                                },
                                "Python error already thrown");
                        });
                    })
        .def("__str__", [](const arb::network_value& v) { return util::pprintf("<arbor.network_value: {}>", v); })
        .def("__repr__", [](const arb::network_value& v) { return util::pprintf("{}", v); });

    network_description
        .def(py::init([](const std::string& selection,
                         const std::string& weight,
                         const std::string& delay,
                         const std::unordered_map<std::string,
                                                  std::variant<std::string, arb::network_selection, arb::network_value>>& map) {
            arb::network_label_dict dict;
            for (const auto& [label, v]: map) {
                const auto& dict_label = label;
                std::visit(
                    arb::util::overload(
                        [&](const std::string& s) {
                            auto sel = arborio::parse_network_selection_expression(s);
                            if (sel) {
                                dict.set(dict_label, *sel);
                                return;
                            }

                            auto val = arborio::parse_network_value_expression(s);
                            if (val) {
                                dict.set(dict_label, *val);
                                return;
                            }

                            throw pyarb_error(util::strprintf("Failed to parse \"{}\" label in dict of network description.\n"
                                                              "Selection label parse error:\n {}\n"
                                                              "Value label parse error:\n{}",
                                                              dict_label,
                                                              sel.error().what(),
                                                              val.error().what()));
                        },
                        [&](const arb::network_selection& sel) { dict.set(dict_label, sel); },
                        [&](const arb::network_value& val) { dict.set(dict_label, val); }),
                    v);
            }
            auto desc = arb::network_description{
                    arborio::parse_network_selection_expression(selection).unwrap(),
                    arborio::parse_network_value_expression(weight).unwrap(),
                    arborio::parse_network_value_expression(delay).unwrap(),
                    dict};
                return desc;
            }),
        "selection"_a, "weight"_a, "delay"_a, "dict"_a,
        "Construct network description.");
}

}  // namespace pyarb
