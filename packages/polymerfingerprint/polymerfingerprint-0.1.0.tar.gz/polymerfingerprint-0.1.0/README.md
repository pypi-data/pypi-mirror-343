# polymerfingerprint
## origin
The Polymerfingerprint is a decoder for SMILES of polymer monomer units specialised for machine learning and the product
of a prior scientific study *"Fingerprint applicable for machine learning tested on LCST behavior of polymers"*.
Please cite us under https://doi.org/10.1016/j.xcrp.2023.101553 upon using the code or the data generated with it.<br>
<small>A tutorial to redo the study is available as *"Protocol for creating representations of molecular structures using a
polymer-specific decoder"* (https://doi.org/10.1016/j.xpro.2024.103055)</small>

## Use cases
- creating fingerprints of homo-, or random copolymers
  - the polymerfingerprint consists of morgan and atom pair fingerprints by default
  - constituting fingerprints can be added removed or swapped out
- reducing these sets to gain a concise representation for machine learning

## Example for creating a reducing a fingerprint set
```python
import polymerfingerprint as pfp

# the create fingerprint function can take dataframes or lists of molecules these two serve just as examples
a_polyfingerprint = pfp.create_pfp(end_units={"start": "[C](C)(C)(C#N)", "end": "[S]C(=S)OCC"},
                                   repeating_units={0.53: "[CH2][CH1](OC(=O)C)", 0.47: "[CH2][CH](N1C(=O)CCCCC1)"},
                                   mol_weight=35370,
                                   fp_size=2048)

b_polyfingerprint = pfp.create_pfp(end_units={"start": "[C](C=C)(C)(C#N)", "end": "[S]C(=S)OCCCC"},
                                       repeating_units={0.53: "[CH2][CH1](OC(=O)CC)", 0.47: "[CH2][CH](N1C(=O)CCC1)"},
                                       mol_weight=35370, fp_size=2048)

# create a list of polymerfingerprints
list_of_pfps = [a_polyfingerprint, b_polyfingerprint]

reduced_set = pfp.reduce_fp_set(∗list_of_pfps)
```
