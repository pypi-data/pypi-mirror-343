.. _pyinterconnectivity:

Interconnectivity
#################

.. currentmodule:: arbor

.. class:: connection

    Describes a connection between two cells, defined by source and target end points (that is presynaptic and
    postsynaptic respectively), a connection weight, and a delay time.

    The :attr:`target` does not include the gid of a cell, this is because a :class:`arbor.connection` is bound to the
    target cell, which means that the gid is implicitly known.

    .. function:: connection(source, target, weight, delay)

        Construct a connection between the :attr:`source` and the :attr:`target` with a :attr:`weight` and :attr:`delay`.

    .. attribute:: source

        The source end point of the connection (type: :class:`arbor.cell_global_label`, which can be initialized with a
        (gid, label) or a (gid, (label, policy)) tuple. If the policy is not indicated, the default
        :attr:`arbor.selection_policy.univalent` is used).

    .. attribute:: target

        The target end point of the connection (type: :class:`arbor.cell_local_label` representing the label of the
        target on the cell, which can be initialized with just a label, in which case the default
        :attr:`arbor.selection_policy.univalent` is used, or a (label, policy) tuple). The gid of the cell is
        implicitly known.

    .. attribute:: weight

        The weight delivered to the target synapse. It is up to the target mechanism to interpret this quantity.
        For Arbor-supplied point processes, such as the ``expsyn`` synapse, a weight of ``1`` corresponds to an
        increase in conductivity in the target mechanism of ``1`` μS (micro-Siemens).

    .. attribute:: delay

        The delay time of the connection [ms]. Must be positive and finite.

    .. note::

        A minimal full example of a connection reads as follows:
        (see :ref:`network tutorial <tutorialnetworkring>` for a more comprehensive example):

        .. code-block:: python

            import arbor as A
            from arbor import units as U 

            # Create two locset labels, describing the endpoints of the connection.
            labels = A.label_dict()
            labels['synapse_site'] = '(location 1 0.5)'
            labels['root'] = '(root)'

            # Place 'expsyn' mechanism on "synapse_site", and a threshold detector at "root"
            decor = A.decor()
            decor.place('"synapse_site"', 'expsyn', 'syn')
            decor.place('"root"', arbor.threshold_detector(-10), 'detector')

            # Implement the connections_on() function on a recipe as follows:
            def connections_on(gid):
               # construct a connection from the "detector" source label on cell 2
               # to the "syn" target label on cell gid with weight 0.01 and delay of 10 ms.
               source  = (2, "detector") # gid and locset label of the source
               target = "syn" # gid of the target is determined by the argument to `connections_on`.
               weight = 0.01  # unit/scaling depends on the synapse used; commonly chosen as μS 
               d    = 10 * U.ms # delay
               return [arbor.connection(source, target, weight, delay)]

.. class:: gap_junction_connection

    Describes a gap junction between two gap junction sites.

    The :attr:`local` site does not include the gid of a cell, this is because a :class:`arbor.gap_junction_connection`
    is bound to the target cell which means that the gid is implicitly known.

    .. note::

       A bidirectional gap-junction between two cells ``c0`` and ``c1`` requires two
       :class:`gap_junction_connection` objects to be constructed: one where ``c0`` is the
       :attr:`local` site, and ``c1`` is the :attr:`peer` site; and another where ``c1`` is the
       :attr:`local` site, and ``c0`` is the :attr:`peer` site.

    .. function::gap_junction_connection(peer, local, weight)

        Construct a gap junction connection between :attr:`peer` and :attr:`local` with weight :attr:`weight`.

    .. attribute:: peer

        The gap junction site: the remote half of the gap junction connection (type: :class:`arbor.cell_global_label`,
        which can be initialized with a (gid, label) or a (gid, label, policy) tuple. If the policy is not indicated,
        the default :attr:`arbor.selection_policy.univalent` is used).

    .. attribute:: local

        The gap junction site: the local half of the gap junction connection (type: :class:`arbor.cell_local_label`
        representing the label of the target on the cell, which can be initialized with just a label, in which case
        the default :attr:`arbor.selection_policy.univalent` is used, or a (label, policy) tuple). The gid of the
        cell is implicitly known.

    .. attribute:: weight

        The unit-less weight of the gap junction connection.

.. class:: threshold_detector

    A threshold detector, generates a spike when voltage crosses a threshold. Can be used as source endpoint for an
    :class:`arbor.connection`.

    .. attribute:: threshold

        Voltage threshold of threshold detector [mV]


.. class:: network_site_info

    A network connection site on a cell. Used for generated connections through the high-level network description.

    .. attribute:: gid

        The cell index.

    .. attribute:: kind

        The cell kind.

    .. attribute:: label

        The associated label.

    .. attribute:: location

        The local location on the cell.

    .. attribute:: global_location

        The global location in cartesian coordinates.


.. class:: network_connection_info

    A network connection between cells. Used for generated connections through the high-level network description.

    .. attribute:: source

        The source connection site.

    .. attribute:: target

        The target connection site.


.. class:: network_description

    A complete network description required for processing.

    .. attribute:: selection

        Selection of connections.

    .. attribute:: weight

        Weight of generated connections.

    .. attribute:: delay

        Delay of generated connections.

    .. attribute:: dict

        Dictionary for named selecations and values.


.. function:: generate_network_connections(recipe, context = None, decomp = None)

        Generate network connections from the network description in the recipe. A distributed context and
        domain decomposition can optionally be provided. Only generates connections with local gids in the
        domain composition as the target. Will return all connections on every process, if no context and domain
        decomposition are provided. Does not include connections from the "connections_on" recipe function.
