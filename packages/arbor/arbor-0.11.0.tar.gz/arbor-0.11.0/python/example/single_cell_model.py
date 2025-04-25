#!/usr/bin/env python3
# This script is included in documentation. Adapt line numbers if touched.

import arbor as A
from arbor import units as U
import pandas as pd  # You may have to pip install these.
import seaborn as sns  # You may have to pip install these.

# (1) Create a morphology with a single (cylindrical) segment of length=diameter=6 μm
tree = A.segment_tree()
tree.append(A.mnpos, A.mpoint(-3, 0, 0, 3), A.mpoint(3, 0, 0, 3), tag=1)

# (2) Define the soma and its midpoint
labels = A.label_dict({"soma": "(tag 1)", "midpoint": "(location 0 0.5)"})

# (3) Create and set up a decor object
decor = (
    A.decor()
    .set_property(Vm=-40 * U.mV)
    .paint('"soma"', A.density("hh"))
    .place('"midpoint"', A.iclamp(10 * U.ms, 2 * U.ms, 0.8 * U.nA), "iclamp")
    .place('"midpoint"', A.threshold_detector(-10 * U.mV), "detector")
)

# (4) Create cell and the single cell model based on it
cell = A.cable_cell(tree, decor, labels)

# (5) Make single cell model.
m = A.single_cell_model(cell)

# (6) Attach voltage probe sampling at 10 kHz (every 0.1 ms).
m.probe("voltage", '"midpoint"', tag="Um", frequency=10 * U.kHz)

# (7) Run simulation for 30 ms of simulated activity.
m.run(tfinal=30 * U.ms)

# (8) Print spike times.
print("{} spikes:".format(len(m.spikes)))
for s in m.spikes:
    print(f" * {s:3.3f} ms")

# (9) Plot the recorded voltages over time.
print("Plotting results ...")
sns.set_theme()  # Apply some styling to the plot
df = pd.DataFrame({"t/ms": m.traces[0].time, "U/mV": m.traces[0].value})
sns.relplot(data=df, kind="line", x="t/ms", y="U/mV", errorbar=None).savefig(
    "single_cell_model_result.svg"
)

# (10) Optionally, you can store your results for later processing.
df.to_csv("single_cell_model_result.csv", float_format="%g")
