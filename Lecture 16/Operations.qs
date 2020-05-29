namespace parityHalving {

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Oracles;
    open Microsoft.Quantum.Arithmetic;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Measurement;

    // prepare |x> from x
    operation prepareInput(x: Bool[], qs: Qubit[]): Unit {
        let len = Length(x);
        for (i in 0 .. len - 1) {
            if (x[i]) {
                X(qs[i]);
            }
        }
    }

    // creates a GHZ state in qs on all qubits
    operation createGHZ(qs: Qubit[]): Unit {
        let numQubits = Length(qs);
        H(qs[0]);
        for (i in 1 .. numQubits - 1) {
            CNOT(qs[0], qs[i]);
        }
    }

    // creates poor man's cate state in qs, stores parities in parityQs
    operation createPoorMansCatState(qs: Qubit[], parityQs: Qubit[]): Result[] {
        let numQubits = Length(qs);

        // apply Hadamards to create |+> states 
        ApplyToEach(H, qs);

        // take parities of pairs of |+> states and put them in parityQs
        // we do this in 2 layers
        for (i in 0 .. numQubits - 2) {
            CNOT(qs[i], parityQs[i]);
        }
        for (i in 1 .. numQubits - 1) {
            CNOT(qs[i], parityQs[i - 1]);
        }

        // measure parity qubits; remaining states should be poor man's cat state
        let res = MultiM(parityQs);

        return res;
    }

    // solve Parity-Halving-Problem
    operation solvePHP(x: Bool[]): Result[] {
        let len = Length(x);
        let numQubits = 2 * len;
        mutable res = new Result[len];

        using (qs = Qubit[numQubits]) {
            let refQs = qs[0 .. len - 1];
            let GHZqs = qs[len .. numQubits - 1];

            prepareInput(x, refQs);
            createGHZ(GHZqs);

            for (i in 0 .. len - 1) {
                Controlled(S)([refQs[i]], GHZqs[i]);
            }

            ApplyToEach(H, GHZqs);
            set res = MultiM(GHZqs);
            ResetAll(qs);
        }

        return res;
    }

    // solve relaxed Parity-Halving-Problem
    operation solveRPHP(x: Bool[]): (Result[], Result[]) {
        let len = Length(x);
        let numQubits = 3 * len - 1;
        mutable res = new Result[len];
        mutable parities = new Result[len - 1];        

        using (qs = Qubit[numQubits]) {
            let refQs = qs[0 .. len - 1];
            let catQs = qs[len .. 2 * len - 1];
            let parityQs = qs[2 * len .. numQubits - 1];

            prepareInput(x, refQs);
            set parities = createPoorMansCatState(catQs, parityQs);

            for (i in 0 .. len - 1) {
                Controlled(S)([refQs[i]], catQs[i]);
            }

            ApplyToEach(H, catQs);
            set res = MultiM(catQs);
            ResetAll(qs);
        }

        return (res, parities);
    }
}
