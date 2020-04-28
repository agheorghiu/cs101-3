namespace orderFinding {

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Oracles;
    open Microsoft.Quantum.Arithmetic;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Convert;


    // maps |y> to |g^{2^pow2} * y mod N>
    operation pow2ModExp(g: Int, pow2: Int, N: Int, y: Qubit[]) : Unit is Adj + Ctl {
        let qs = (LittleEndian)(y);
        let pow = 1 <<< pow2;
        let op = OperationPowCA(MultiplyByModularInteger(g, N, _), pow);
        op(qs);
    }

    // maps |x>|y> to |x>|g^x * y mod N>
    operation modularExp(g: Int, N: Int, x: Qubit[], y: Qubit[]) : Unit {
        let n = Length(x);
        for (i in 0 .. n - 1) {
            let op = pow2ModExp(g, i, N, _);
            (Controlled op)([x[i]], y);
        }
    }

    // outputs res such that res/N is approximately m/k, where k is the order of g
    // and m is some positive integer
    // here n is the number of qubits for one register (there will be 2n in total)
    operation orderFindingHelper(g: Int, N: Int, n: Int) : Int {
        mutable res = 0;

        using (qs = Qubit[2 * n]) {
            let x = qs[0 .. n - 1];
            let y = qs[n .. 2 * n - 1];

            // initialize |y> as |10...0> (which is 1 in the little-endian integer representation)
            X(y[0]);

            // create superposition over all x values
            ApplyToEach(H, x);

            // create state sum_x |x>|g^x mod N>
            modularExp(g, N, x, y);

            // apply QFT to first register
            ApplyQuantumFourierTransform(LittleEndian(x));

            // measure first register
            set res = MeasureInteger(LittleEndian(x));

            ResetAll(qs);
        }

        return res;
    }

}