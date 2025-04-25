.. _formatswc:

SWC
~~~

.. csv-table::
   :header: "Name", "File extension", "Read", "Write"

   "SWC", "``swc``", "✓", "✗"

Arbor supports reading morphologies described using the
`SWC <http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html>`_ file format.

SWC files may contain comments, which are stored as metadata. And a blank line anywhere in the file is
interpreted as the end of data.

The description of the morphology is encoded as a list of samples with an id,
an `x,y,z` location in space, a radius, a tag, and a parent id. Arbor parses these samples, performs some checks,
and then generates a morphology according to one of three possible interpretations.

The SWC file format specifications do not describe how the file should be interpreted to reconstruct
a morphology from SWC samples. This has led different simulators to interpret SWC files in different
ways, specifically the reconstruction of the soma. Arbor has its own interpretation that
is powerful and simple to understand at the same time. However, we have also developed functions that will
interpret SWC files similarly to how the NEURON simulator would.

Despite the differences between the interpretations, there is a common set of checks that are always performed
to validate an SWC file:

* Check that there are no duplicate ids.
* Check that the parent id of a sample is less than the id of the sample.
* Check that the parent id of a sample refers to an existing sample.

In addition, all interpretations agree that a *segment* is (in the common case) constructed between a sample and
its parent and inherits the tag of the sample; and if more than one sample has the same parent, the parent sample
is interpreted as a fork point in the morphology, and acts as the proximal point to a new branch for each of its
"child" samples. There a couple of exceptions to these rules which are listed below.

.. Note::

   The SWC file format allows the association of ``tags`` with parts of the
   morphology and reserves tag values 1-4 for soma, axon, basal dendrite, and
   apical dendrite. In Arbor, these tags can be added to a
   :class:`arbor.label_dict` using the :meth:`~arbor.label_dict.add_swc_tags` method.


.. _formatswc-arbor:

Arbor interpretation
""""""""""""""""""""
In addition to the previously listed checks, the arbor interpretation explicitly disallows SWC files where the soma is
described by a single sample. It constructs the soma from 2 or more samples, forming 1 or more segments. A *segment* is
always constructed between a sample and its parent. This means that there are no gaps in the resulting morphology.

Arbor has no magic rules or transformations for the soma. It can be a single branch or multiple branches; segments
of a different tag can connect to its distal end, proximal end, or anywhere in the middle. For example, to create a
morphology with a single-segment soma, a single-segment axon connected to one end of the soma, and a single-segment
dendrite connected to the other end of the soma, the following swc file can be used:


.. literalinclude :: example.swc
   :language: python
   :linenos:

Samples 1 and 2 will form the soma; samples 1 and 3 will form the axon, connected to the soma at the proximal end;
samples 2 and 4 will form the dendrite, connected to the soma at the distal end. The morphology will look like something
like this:

.. figure:: ../gen-images/swc_morph.svg
   :width: 400
   :align: center

.. _formatswc-neuron:

NEURON interpretation
"""""""""""""""""""""
Arbor provides support for interpreting SWC inputs in the same way as NEURON,
to ease the porting of cell models developed in NEURON to Arbor.

The NEURON interpretations are based on the observed output of NEURON's ``Import3d_SWC_read``
function, which is based on the `Neuromorpho approach <http://neuromorpho.org/SomaFormat.html>`_.
However, there are differences and undocumented interpretations of the soma and how dendrites,
axons and apical dendrites are attached to it that are not described explicitly by Neuromorpho.

.. Warning::

   The interpretation of SWC files by NEURON's import 3D method changed in NEURON
   8 to address bugs in earlier versions. Arbor follows the NEURON 8 approach,
   and can't guarantee compatibility with reconstructed SWC morphologies from NEURON 7.

.. Note::

    The rules below are applied to the morphology representation only when a soma
    sample is present, otherwise the default
    :ref:`Arbor interpretation <formatswc-arbor>` is applied.

**Every sample must have the same SWC identifier (tag) as its parent, except for
samples whose parent is tagged as soma**:
This enforces that axonal and dendritic segments can only attach to the soma.
Conversely, it isn't possible to attach an axon to a dendrite, for example.

**The first sample is tagged as soma**:
This requirement is a corollary of the previous rule.

**Single-sample somas are permitted**:
The `Neuromorpho guidelines <http://neuromorpho.org/SomaFormat.html>`_ regarding
interpretation of a spherical soma described with a single soma sample can be summarised:

* The soma is composed of two cylinders that have their proximal ends at the soma
  center, extended first along the negative y-axis and then the positive y-axis.

Following the Neuromorpho specification, NEURON constructs the soma from two cylinders,
joined at the soma center. It differs in two ways:

* The soma is extended along the x-axis, not the y-axis.
* The soma is constructed from three points, the first at ``x=x0-r``, the second with
  ``x=x0`` and the third at ``x=x0+r``, to form a single section.
* All dendrites, axons, and apical dendrites are attached to the center of the soma with "zero resistance wires".

**The axon, dendrite, and apical sub-trees follow special rules for attachment to
the soma**: By default, the sub-tree starts at the first sample with the
a tag indicating a non-soma segment, and not at the parent location on the soma, and
the sub-tree is connected to its parent with a "zero resistance wire".
**Except** when the sub-tree is defined by a single child sample. In which case
the sub-tree is composed of a single segment from the parent location on the
soma to the child sample, with a constant radius of the child.

Note that these special properties can lead to unintuitive behaviour in some cases. Example

.. code-block::

     # id, tag, x, y, z, radius, parent
     1     1    0  0  0  6       -1
     2     3    2  0  0  3        1

As we have one sample tagged ``1`` (soma), the soma is built by two cylinders
approximating a sphere. The dendrite is attached to the center, thus, the
morphology has *three* branches arranged in a 'T'-shape.

API
"""

* :ref:`Python <pyswc>`
* :ref:`C++ <cppswc>`
