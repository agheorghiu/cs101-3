namespace linearSysSolver {

    open Microsoft.Quantum.Canon;
    open Microsoft.Quantum.Intrinsic;
    open Microsoft.Quantum.Oracles;
    open Microsoft.Quantum.Arithmetic;
    open Microsoft.Quantum.Diagnostics;
    open Microsoft.Quantum.Convert;
    open Microsoft.Quantum.Math;
    open Microsoft.Quantum.Measurement;

    // define data type for matrix obtained through linear combination of unitaries
    newtype LCUMatrix = (Coeffs: Double[], Paulis: Pauli[][]);

    // define data type for a Fourier series that includes the coefficients of the terms
    // and the coefficients in the exponents
    newtype FourierSeries = (Coeffs: Double[], ExpCoeffs: Double[]);


    // return the Trotter number we're considering 
    function getTrotterNumber(): Double {
        return 100.;
    }

    // reverses the bits in n
    function reverseBinRep(n: Int, numBits: Int): Int {
        let boolRep = IntAsBoolArray(n, numBits);
        return BoolArrayAsInt(boolRep[numBits - 1 .. -1 .. 0]);
    }

    // return the square roots of the absolute values of the elements of an array
    function sqrtAll(v: Double[]): Double[] {
        let n = Length(v);
        mutable sqrtV = new Double[n];
        for (i in 0 .. n - 1) {
            set sqrtV w/= i <- Sqrt(AbsD(v[i]));
        }
        return sqrtV;
    }

    // arccos for a fraction
    function arccosFrac(num: Double, denom: Double): Double {
        if (denom <= 1e-10) {
            return 0.;
        }
        return ArcCos(num / denom);
    }


    // create the state |phi(x)> = \sum_i |x_i| |i>, for suitably normalized x_i's
    // we're assuming Length(x) is a power of 2
    operation encodeState(x: Double[], qs: Qubit[]): Unit is Adj + Ctl {
        let n = Length(x);
        let numQubits = Length(qs);

        if (n > 1) {
            let xL = x[0 .. n / 2 - 1];
            let xR = x[n / 2 .. n - 1];
            let norm = Sqrt(SquaredNorm(x));
            let normL = Sqrt(SquaredNorm(xL));

            // angle by which we Y rotate the 0'th qubit
            let angle = 2. * arccosFrac(normL, norm);

            // rotate that qubit to put it in the superposition |L||0> + |R||1>
            Ry(angle, qs[0]);

            // create controlled unitaries to recursively prepare the rest of the state
            let ctrlL = ControlledOnInt(0, encodeState(xL, _));
            let ctrlR = ControlledOnInt(1, encodeState(xR, _));

            // prepare encoded state
            ctrlL([qs[0]], qs[1 .. numQubits - 1]);
            ctrlR([qs[0]], qs[1 .. numQubits - 1]);
        }
    }

    // create the state |phi(x)> = \sum_i x_i |i>, for suitably normalized x_i's
    // we're assuming Length(x) is a power of 2
    operation encodeStateWithSigns(x: Double[], sgnQubit: Qubit, qs: Qubit[]): Unit is Adj + Ctl {
        let n = Length(x);
        let numQubits = Length(qs);

        // encode state without signs
        encodeState(x, qs);

        // add signs
        X(sgnQubit);
        for (i in 0 .. n - 1) {
            if (x[i] < 0.) {
                (ControlledOnInt(reverseBinRep(i, numQubits), Z))(qs, sgnQubit);
            }
        }
        X(sgnQubit);
    }

    // test function for state encoding
    operation testEnc(): Unit {
        let x = [-0.1, -0.1, 0.4, 0., 0.8, -0.2, 0., 0.];
        let numQubits = 3;

        using(qs = Qubit[numQubits + 1]) {
            encodeStateWithSigns(x, qs[numQubits], qs[numQubits - 1 .. -1 .. 0]);
            //encodeState(x, qs[numQubits - 1 .. -1 .. 0]);
            DumpRegister((), qs[0 .. numQubits - 1]);
            ResetAll(qs);
        }
    }

    // applies \prod_i exp(theta * coeffs[i]/n * paulis[i]) to qs
    operation trotterLCPHelper(n: Double, theta: Double, coeffs: Double[], paulis: Pauli[][], qs: Qubit[]): Unit is Adj + Ctl {
        let numQubits = Length(qs);
        let numPaulis = Length(paulis);

        for (i in 0 .. numPaulis - 1) {
            Exp(paulis[i], theta * coeffs[i] / n, qs);
        }
    }

    // performs approximate version of exp(\sum_i theta * coeffs[i] paulis[i])
    // uses first-order Troterrization
    operation trotterLCP(n: Double, theta: Double, coeffs: Double[], paulis: Pauli[][], qs: Qubit[]): Unit is Adj + Ctl {
        (OperationPowCA(trotterLCPHelper(n, theta, coeffs, paulis, _), Floor(n)))(qs);
    }

    // test function for Troterrization
    operation testExp(): Unit {
        let x = [1. / Sqrt(2.), 1. / Sqrt(2.)];
        let coeffs = [1. / Sqrt(2.), 1. / Sqrt(2.)];
        let paulis = [[PauliX], [PauliZ]];

        using (qs = Qubit[1]) {
            encodeState(x, qs);
            X(qs[0]);
            trotterLCP(getTrotterNumber(), PI() / 2., coeffs, paulis, qs);
            DumpMachine();
            ResetAll(qs);
        }        
    }

    // create block encoded unitary as a linear combination of unitaries
    operation blockEncoder(coeffs: Double[], unitaries: (Qubit[] => Unit is Adj + Ctl)[], sgnQubit: Qubit, qs: Qubit[]): Unit is Adj + Ctl {
        let n = Length(unitaries);
        let numQubits = Length(qs);
        let numAncilla = Ceiling(Lg(IntAsDouble(n)));
        let sqrtCoeffs = sqrtAll(coeffs);

        X(sgnQubit);
        encodeState(sqrtCoeffs, qs[0 .. numAncilla]);
        for (i in 0 .. n - 1) {
            if (coeffs[i] < 0.) {
                (ControlledOnInt(reverseBinRep(i, numAncilla), Z))(qs[0 .. numAncilla -1], sgnQubit);
            }
            (ControlledOnInt(reverseBinRep(i, numAncilla), unitaries[i]))(qs[0 .. numAncilla - 1], qs[numAncilla .. numQubits - 1]);
        }
        Adjoint(encodeState(sqrtCoeffs, _))(qs[0 .. numAncilla]);
        X(sgnQubit);
    }

    // test function for block encoding
    operation testBlockEncoder() : Unit {
        let numQubits = 2;
        let coeffs = [Cos(PI() / 8.), -Sin(PI() / 8.)];
        let unitaries = [ApplyToEachCA(I, _), ApplyToEachCA(X, _)];

        using (qs = Qubit[numQubits + 1]) {
            let sgnQubit = qs[numQubits];
            let rqs = qs[numQubits - 1 .. -1 .. 0];
            blockEncoder(coeffs, unitaries, sgnQubit, rqs);
            DumpRegister((), qs[0 .. numQubits - 1]);
            Message("");
            Message("");           
            ResetAll(qs);

            X(qs[0]);
            blockEncoder(coeffs, unitaries, sgnQubit, rqs);
            DumpRegister((), qs[0 .. numQubits - 1]);           
            Message("");
            Message("");
            ResetAll(qs);

            X(qs[1]);
            blockEncoder(coeffs, unitaries, sgnQubit, rqs);
            DumpRegister((), qs[0 .. numQubits - 1]);
            Message("");
            Message("");           
            ResetAll(qs);

            ApplyToEach(X, qs[0 .. numQubits - 1]);
            blockEncoder(coeffs, unitaries, sgnQubit, rqs);
            DumpRegister((), qs[0 .. numQubits - 1]);
            Message("");
            Message("");           
            ResetAll(qs);
        }
    }

    // the HHL algorithm
    operation hhlSolver(A: LCUMatrix, enc: ((Qubit, Qubit[]) => Unit is Adj + Ctl), inv: FourierSeries, qs: Qubit[]) : Unit {
        let coeffsA = A::Coeffs;
        let paulisA = A::Paulis;

        // we're assuming the lengths of these is a power of 2
        let coeffsInv = inv::Coeffs;
        let expCoeffsInv = inv::ExpCoeffs;
        let seriesLen = Length(coeffsInv);

        // create unitaries for series linear combination
        mutable unitaries = new (Qubit[] => Unit is Adj + Ctl)[seriesLen];
        for (i in 0 .. seriesLen - 1) {
            set unitaries w/= i <- trotterLCP(getTrotterNumber(), expCoeffsInv[i], coeffsA, paulisA, _);
        }

        // create the required number of qubits
        let numAncillas = Floor(Lg(IntAsDouble(seriesLen))) + 1; // extra qubit for signs        
        let numRefQubits = Length(paulisA[0]);
        let numQubits = Length(qs);

        // group qubits
        let sgnQubit = qs[0];
        let ancillas = qs[1 .. numAncillas - 1];
        let refQs = qs[numAncillas .. numQubits - 1];
        let rqs = qs[1 .. numQubits - 1];

        // apply state encoding
        enc(sgnQubit, refQs);

        // apply the unitary that should have an approximation of A^{-1} block-encoded
        blockEncoder(coeffsInv, unitaries, sgnQubit, rqs);
    }

    // function for testing HHL
    operation testHHL(seriesCoeffs: Double[], expCoeffs: Double[]): (Int, Result[]) {
        // create input matrix
        let coeffs = [Cos(PI() / 10.), Sin(PI() / 10.)];
        let paulis = [[PauliX], [PauliI]];
        let A = LCUMatrix(coeffs, paulis);

        // create input vector
        let x = [1., 0.];
        let encX = encodeStateWithSigns(x, _, _);

        // Fourier series to apply
        let fourierSeries = FourierSeries(seriesCoeffs, expCoeffs);
        let seriesLen = Length(seriesCoeffs);

        // group qubits
        let numAncillas = Floor(Lg(IntAsDouble(seriesLen))) + 1;
        let numRefQubits = 1;
        let numQubits = numAncillas + numRefQubits;
        mutable ancRes = 0;
        mutable res = new Result[numRefQubits];

        using (qs = Qubit[numQubits]) {
            let refQs = qs[numAncillas .. numQubits - 1];
            let ancillas = qs[1 .. numAncillas - 1];
            hhlSolver(A, encX, fourierSeries, qs);

            set ancRes = MeasureInteger(LittleEndian(ancillas));
            set res = MultiM(refQs);
            ResetAll(qs);
        }

        return (ancRes, res);
    }

}

