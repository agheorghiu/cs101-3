namespace groverSearch {

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Oracles;
    open Microsoft.Quantum.Arithmetic;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Measurement;

    // Grover oracle that flips last qubit only if first qubits encode the number n
    operation intOracle(n: Int, qs: Qubit[]): Unit {
        let numQubits = Length(qs);        
        (ControlledOnInt(n, X))(qs[0 .. numQubits - 2], qs[numQubits - 1]);
    }

    // performs reflection about \sum_x |x>, where x is on n bits; qs has n + 1 qubits (last is used for phase flips)
    operation groverDiffusion(qs: Qubit[]): Unit {
        let numQubits = Length(qs);
        ApplyToEach(H, qs[0 .. numQubits - 2]);
        (ControlledOnInt(0, X))(qs[0 .. numQubits - 2], qs[numQubits - 1]);
        ApplyToEach(H, qs[0 .. numQubits - 2]);        
    }

    // Grover's search algorithm; qs has n + 1 qubits, the last qubit is used to perform phase flips
    operation groverSearch(oracle: (Qubit[] => Unit), qs: Qubit[]): Unit {
        let numQubits = Length(qs);
        let numIter = Floor((PI() / 4.) * 2. ^(IntAsDouble(numQubits - 1) / 2.));

        // make last qubit |-> to perform phase flips
        X(qs[numQubits - 1]);
        H(qs[numQubits - 1]);

        // create superposition over all inputs
        ApplyToEach(H, qs[0 .. numQubits - 2]);

        // perform O(2^(numQubits - 1)/2) Grover reflections
        for (i in 1 .. numIter) {
            oracle(qs);
            groverDiffusion(qs);
        }
    }

    // test function for state encoding
    operation runGrover(n: Int, numQubits: Int): Result[] {
        mutable res = new Result[numQubits - 1];

        using(qs = Qubit[numQubits]) {
            groverSearch(intOracle(n, _), qs);
            set res = MultiM(qs[0 .. numQubits - 2]);
            ResetAll(qs);
        }

        return res;
    }

}