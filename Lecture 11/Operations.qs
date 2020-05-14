namespace qsimExample {

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Oracles;
    open Microsoft.Quantum.Arithmetic;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Measurement;

    operation hamSim(time : Double) : (Int, Int) {
        let numRuns = 100;
        mutable countsIndep00 = 0;
        mutable countsCorr00 = 0;

        using(qs = Qubit[2]){
            let pauliString = [PauliX, PauliX];

            for (i in 1 .. numRuns) {

                // time evolve each qubit by exp(-itX / 2)
                Exp([PauliX, PauliI], -time / 2., qs);
                Exp([PauliI, PauliX], -time / 2., qs);

                let resI0 = M(qs[0]);
                let resI1 = M(qs[1]);

                if (resI0 == Zero and resI1 == One) {
                    set countsIndep00 = countsIndep00 + 1;
                }

                ResetAll(qs);          

                // time evolve both qubits by exp(-it X \otimes X / 2)
                Exp(pauliString, -time / 2., qs);

                let resC0 = M(qs[0]);
                let resC1 = M(qs[1]);

                if (resC0 == Zero and resC1 == One) {
                    set countsCorr00 = countsCorr00 + 1;
                }  

                ResetAll(qs);
            }
        }
        return (countsIndep00, countsCorr00);
    }

}
