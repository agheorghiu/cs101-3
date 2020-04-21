namespace TestStuff
{
    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Convert;

    operation HelloQ () : Unit {
        using (qs = Qubit[2]) {
            let count = 1000;
            mutable numOnes = 0;

            for (i in 1 .. count) {
                H(qs[0]);
                CNOT(qs[0], qs[1]);

                H(qs[0]);

                let res0 = M(qs[0]); // Result.One, Result.Zero
                let res1 = M(qs[1]);
                if (res0 == One) {
                    set numOnes = numOnes + 1;
                }
                if (res0 != res1) {
                    Message("Oh no...");
                }
                ResetAll(qs);
            }
            Message($"Number of ones is: {IntAsString(numOnes)}");
            //DumpMachine();
            ResetAll(qs);            
        }
    }
}
