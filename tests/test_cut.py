from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from cutqc2.cutqc.cutqc.main import CutQC


def print_counts(circuit, shots=1000):
    circuit = circuit.measure_all(inplace=False)
    sampler = StatevectorSampler()
    results = sampler.run([circuit], shots=shots).result()
    counts = results[0].data.meas.get_counts()
    print(f"{counts=}")


def test_cut():
    """
    Create a simple 3 qubit circuit and cut it.
    As long as we're able to perform a cut, we're good for now.
    """
    qc = QuantumCircuit(3)
    qc.reset(0)
    qc.reset(1)
    qc.reset(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    print(qc)

    # 000 - 50%, 111 - 50%
    print_counts(qc)

    cutqc = CutQC(
        circuit=qc,
        cutter_constraints={
            "max_subcircuit_width": 2,
            "max_subcircuit_cuts": 1,
            "subcircuit_size_imbalance": 1,
            "max_cuts": 1,
            "num_subcircuits": [2],
        },
        verbose=True,
    )
    cutqc.cut()

    subcircuit0, subcircuit1 = cutqc.cut_solution["subcircuits"]
    print(subcircuit0)
    print_counts(subcircuit0)
    print(subcircuit1)
    print_counts(subcircuit1)

    cutqc.evaluate(num_shots_fn=None)
    cutqc.build(mem_limit=10, recursion_depth=3)
    cutqc.verify()
