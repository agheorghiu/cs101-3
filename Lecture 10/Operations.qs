namespace randomCircuit {

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Oracles;
    open Microsoft.Quantum.Arithmetic;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Measurement;

    // Run a circuit on numQubits with layers of single-qubit and two-qubit gates specified by the two lists
    // measure output in computational basis and return it
    operation runCircuit(numQubits: Int, singleQubitGates: Int[][], twoQubitGates: (Int, Int)[]): Result[] {
        mutable res = new Result[numQubits];
        let numCycles = Length(twoQubitGates);
        let gates = [Rz(PI()/8., _), Ry(PI()/8., _), Rx(PI()/8., _)];

        using (qs = Qubit[numQubits]) {

            for (i in 0 .. numCycles - 1) {
                for (j in 0 .. numQubits - 1) {
                    let g = gates[singleQubitGates[i][j]];
                    g(qs[j]);
                }
                let (idx1, idx2) = twoQubitGates[i];
                CNOT(qs[idx1], qs[idx2]);
            }
            set res = MultiM(qs);
            ResetAll(qs);
        }

        return res;
    }

    // Same as the function above but output is measured as an integer
    operation runCircuitInt(numQubits: Int, singleQubitGates: Int[][], twoQubitGates: (Int, Int)[]): Int {
        mutable res = 0;
        let numCycles = Length(twoQubitGates);
        let gates = [Rz(PI()/8., _), Ry(PI()/8., _), Rx(PI()/8., _)];

        using (qs = Qubit[numQubits]) {

            for (i in 0 .. numCycles - 1) {
                for (j in 0 .. numQubits - 1) {
                    let g = gates[singleQubitGates[i][j]];
                    g(qs[j]);
                }
                let (idx1, idx2) = twoQubitGates[i];
                CNOT(qs[idx1], qs[idx2]);
            }
            set res = MeasureInteger(LittleEndian(qs));
            ResetAll(qs);
        }

        return res;
    }

}
