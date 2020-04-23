namespace MyAlgorithms
{
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Convert;

    // |x>|y> -> |x>|y + f(x)>

    // f constant 0
    operation constant0(qs: Qubit[]) : Unit {

    }

    // f constant 1
    operation constant1(qs: Qubit[]) : Unit {
        let n = Length(qs);
        X(qs[n - 1]);
    }


    // f balanced |x>|y> -> |x>|y + x^1>
    operation balanced(qs: Qubit[]) : Unit {
        let n = Length(qs);
        CNOT(qs[0], qs[n - 1]);
    }

    operation deutschJozsa(qs: Qubit[], oracle: (Qubit[] => Unit)) : Unit {
        let n = Length(qs);
        X(qs[n - 1]);

        ApplyToEach(H, qs);
        oracle(qs);
        ApplyToEach(H, qs);
    }

    // s = 100...0
    operation bvOracle1(qs: Qubit[]) : Unit {
        let n = Length(qs);
        CNOT(qs[0], qs[n - 1]);
    }

    // s = 100...1
    operation bvOracle2(qs: Qubit[]) : Unit {
        let n = Length(qs);
        CNOT(qs[0], qs[n - 1]);
        CNOT(qs[n - 2], qs[n - 1]);
    }

    // s = 111...1
    operation bvOracle3(qs: Qubit[]) : Unit {
        let n = Length(qs);
        for (i in 0 .. n - 2) {
            CNOT(qs[i], qs[n - 1]);
        }
    }

    operation bernsteinVazirani(qs: Qubit[], oracle: (Qubit[] => Unit)) : Unit {
        let n = Length(qs);
        X(qs[n - 1]);

        ApplyToEach(H, qs);
        oracle(qs);
        ApplyToEach(H, qs);
    }

    // s = 100..0
    operation simonOracle1(qs: Qubit[]): Unit {
        let n = Length(qs) / 2;

        for (i in 1 .. n - 1) {
            CNOT(qs[i], qs[n + i]);
        }
    }

    // s = 000..1
    operation simonOracle2(qs: Qubit[]): Unit {
        let n = Length(qs) / 2;

        for (i in 0 .. n - 2) {
            CNOT(qs[i], qs[n + i]);
        }
    }


    operation simonSolution(qs: Qubit[], oracle: (Qubit[] => Unit)): Unit {
        let n = Length(qs) / 2;

        ApplyToEach(H, qs[0 .. n - 1]); // sum_x |x>|0>
        oracle(qs); // apply U_f
        ApplyToEach(H, qs[0 .. n - 1]);
    }


    operation Main() : Bool[] {
        let n = 4;
        mutable bits = new Bool[n];
        using(qs = Qubit[2 * n]) {
            simonSolution(qs, simonOracle2);

            mutable res = 0;
            for (i in 0 .. n - 1) {
                set bits w/= i <- ResultAsBool(M(qs[i]));
            }

            ResetAll(qs);
        }

        return bits;
    }
}
