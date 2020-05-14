namespace phaseEstimation {

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Oracles;
    open Microsoft.Quantum.Arithmetic;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Measurement;

    // apply exp(i theta ZI..I)
    operation myHamiltonian(qs: Qubit[]): Unit is Adj + Ctl {
        let theta = 2. * PI() * 0.75;
        Exp([PauliZ], theta, [qs[0]]);
    }

    // perform phase estimation on unitary u, acting on qubits in qs
    operation phaseEstimate(ancilla: Qubit[], qs: Qubit[], u: (Qubit[] => Unit is Adj + Ctl)): Unit {
        let n = Length(qs);
            
        ApplyToEach(H, ancilla);

        for (i in 0 .. n - 1) {
            let pow = 1 <<< i;
            let expU = OperationPowCA(u, pow);
            (Controlled expU)([ancilla[i]], qs);
        }

        ApplyQuantumFourierTransform(LittleEndian(ancilla));
    }

    // perform phase estimation and measure output
    operation runPhaseEstimation(n: Int): Result[] {
        mutable res = new Result[n];

        using(qs = Qubit[2 * n]) {
            //X(qs[n]);
            phaseEstimate(qs[0 .. n - 1], qs[n .. 2 * n - 1], myHamiltonian);
            set res = MultiM(qs[0 .. n - 1]);
            ResetAll(qs);
        }

        return res;
    }

}
