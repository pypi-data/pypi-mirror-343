from math import pi

from pygridsynth import DOmegaUnitary, decompose_domega_unitary

from trasyn import synthesize
from trasyn.gates import rz, u
from trasyn.utils import distance

target = u(0.4, 0.2, 0.3)
seq, mat, err = synthesize(
    target,
    30,
    error_threshold=0.001,
    # num_samples=2000,
    num_attempts=10,
    # gpu=False,
    verbose=True,
)
print(seq, err, seq.count("t"))
seq = decompose_domega_unitary(DOmegaUnitary.from_gates(seq.upper()))
print(seq, seq.count("T"))
