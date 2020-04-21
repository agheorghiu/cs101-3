#pragma warning disable 1591
using System;
using Microsoft.Quantum.Core;
using Microsoft.Quantum.Intrinsic;
using Microsoft.Quantum.Simulation.Core;

[assembly: CallableDeclaration("{\"Kind\":{\"Case\":\"Operation\"},\"QualifiedName\":{\"Namespace\":\"TestStuff\",\"Name\":\"HelloQ\"},\"SourceFile\":\"/Users/andrugheorghiu/git/q-code/TestStuff/Operations.qs\",\"Position\":{\"Item1\":7,\"Item2\":4},\"SymbolRange\":{\"Item1\":{\"Line\":1,\"Column\":11},\"Item2\":{\"Line\":1,\"Column\":17}},\"ArgumentTuple\":{\"Case\":\"QsTuple\",\"Fields\":[[]]},\"Signature\":{\"TypeParameters\":[],\"ArgumentType\":{\"Case\":\"UnitType\"},\"ReturnType\":{\"Case\":\"UnitType\"},\"Information\":{\"Affiliation\":{\"Case\":\"EmptySet\"},\"InferredInformation\":{\"IsSelfAdjoint\":false,\"IsIntrinsic\":false}}},\"Documentation\":[]}")]
[assembly: SpecializationDeclaration("{\"Kind\":{\"Case\":\"QsBody\"},\"TypeArguments\":{\"Case\":\"Null\"},\"Information\":{\"Affiliation\":{\"Case\":\"EmptySet\"},\"InferredInformation\":{\"IsSelfAdjoint\":false,\"IsIntrinsic\":false}},\"Parent\":{\"Namespace\":\"TestStuff\",\"Name\":\"HelloQ\"},\"SourceFile\":\"/Users/andrugheorghiu/git/q-code/TestStuff/Operations.qs\",\"Position\":{\"Item1\":7,\"Item2\":4},\"HeaderRange\":{\"Item1\":{\"Line\":1,\"Column\":11},\"Item2\":{\"Line\":1,\"Column\":17}},\"Documentation\":[]}")]
#line hidden
namespace TestStuff
{
    public class HelloQ : Operation<QVoid, QVoid>, ICallable
    {
        public HelloQ(IOperationFactory m) : base(m)
        {
        }

        String ICallable.Name => "HelloQ";
        String ICallable.FullName => "TestStuff.HelloQ";
        protected ICallable<Int64, String> MicrosoftQuantumConvertIntAsString
        {
            get;
            set;
        }

        protected Allocate Allocate
        {
            get;
            set;
        }

        protected IUnitary<(Qubit,Qubit)> MicrosoftQuantumIntrinsicCNOT
        {
            get;
            set;
        }

        protected IUnitary<Qubit> MicrosoftQuantumIntrinsicH
        {
            get;
            set;
        }

        protected ICallable<Qubit, Result> MicrosoftQuantumIntrinsicM
        {
            get;
            set;
        }

        protected ICallable<String, QVoid> MicrosoftQuantumIntrinsicMessage
        {
            get;
            set;
        }

        protected Release Release
        {
            get;
            set;
        }

        protected ICallable<IQArray<Qubit>, QVoid> MicrosoftQuantumIntrinsicResetAll
        {
            get;
            set;
        }

        public override Func<QVoid, QVoid> Body => (__in__) =>
        {
#line hidden
            {
#line 9 "/Users/andrugheorghiu/git/q-code/TestStuff/Operations.qs"
                var qs = Allocate.Apply(2L);
#line hidden
                Exception __arg1__ = null;
                try
                {
#line 10 "/Users/andrugheorghiu/git/q-code/TestStuff/Operations.qs"
                    var count = 1000L;
#line 11 "/Users/andrugheorghiu/git/q-code/TestStuff/Operations.qs"
                    var numOnes = 0L;
#line 13 "/Users/andrugheorghiu/git/q-code/TestStuff/Operations.qs"
                    foreach (var i in new Range(1L, count))
#line hidden
                    {
#line 14 "/Users/andrugheorghiu/git/q-code/TestStuff/Operations.qs"
                        MicrosoftQuantumIntrinsicH.Apply(qs[0L]);
#line 15 "/Users/andrugheorghiu/git/q-code/TestStuff/Operations.qs"
                        MicrosoftQuantumIntrinsicCNOT.Apply((qs[0L], qs[1L]));
#line 17 "/Users/andrugheorghiu/git/q-code/TestStuff/Operations.qs"
                        MicrosoftQuantumIntrinsicH.Apply(qs[0L]);
#line 19 "/Users/andrugheorghiu/git/q-code/TestStuff/Operations.qs"
                        var res0 = MicrosoftQuantumIntrinsicM.Apply(qs[0L]);
#line 20 "/Users/andrugheorghiu/git/q-code/TestStuff/Operations.qs"
                        var res1 = MicrosoftQuantumIntrinsicM.Apply(qs[1L]);
#line 21 "/Users/andrugheorghiu/git/q-code/TestStuff/Operations.qs"
                        if ((res0 == Result.One))
                        {
#line 22 "/Users/andrugheorghiu/git/q-code/TestStuff/Operations.qs"
                            numOnes = (numOnes + 1L);
                        }

#line 24 "/Users/andrugheorghiu/git/q-code/TestStuff/Operations.qs"
                        if ((res0 != res1))
                        {
#line 25 "/Users/andrugheorghiu/git/q-code/TestStuff/Operations.qs"
                            MicrosoftQuantumIntrinsicMessage.Apply("Oh no...");
                        }

#line 27 "/Users/andrugheorghiu/git/q-code/TestStuff/Operations.qs"
                        MicrosoftQuantumIntrinsicResetAll.Apply(qs);
                    }

#line 29 "/Users/andrugheorghiu/git/q-code/TestStuff/Operations.qs"
                    MicrosoftQuantumIntrinsicMessage.Apply(String.Format("Number of ones is: {0}", MicrosoftQuantumConvertIntAsString.Apply(numOnes)));
#line 31 "/Users/andrugheorghiu/git/q-code/TestStuff/Operations.qs"
                    MicrosoftQuantumIntrinsicResetAll.Apply(qs);
                }
#line hidden
                catch (Exception __arg2__)
                {
                    __arg1__ = __arg2__;
                    throw __arg1__;
                }
#line hidden
                finally
                {
                    if (__arg1__ != null)
                    {
                        throw __arg1__;
                    }

#line hidden
                    Release.Apply(qs);
                }
            }

#line hidden
            return QVoid.Instance;
        }

        ;
        public override void Init()
        {
            this.MicrosoftQuantumConvertIntAsString = this.Factory.Get<ICallable<Int64, String>>(typeof(Microsoft.Quantum.Convert.IntAsString));
            this.Allocate = this.Factory.Get<Allocate>(typeof(Microsoft.Quantum.Intrinsic.Allocate));
            this.MicrosoftQuantumIntrinsicCNOT = this.Factory.Get<IUnitary<(Qubit,Qubit)>>(typeof(Microsoft.Quantum.Intrinsic.CNOT));
            this.MicrosoftQuantumIntrinsicH = this.Factory.Get<IUnitary<Qubit>>(typeof(Microsoft.Quantum.Intrinsic.H));
            this.MicrosoftQuantumIntrinsicM = this.Factory.Get<ICallable<Qubit, Result>>(typeof(Microsoft.Quantum.Intrinsic.M));
            this.MicrosoftQuantumIntrinsicMessage = this.Factory.Get<ICallable<String, QVoid>>(typeof(Microsoft.Quantum.Intrinsic.Message));
            this.Release = this.Factory.Get<Release>(typeof(Microsoft.Quantum.Intrinsic.Release));
            this.MicrosoftQuantumIntrinsicResetAll = this.Factory.Get<ICallable<IQArray<Qubit>, QVoid>>(typeof(Microsoft.Quantum.Intrinsic.ResetAll));
        }

        public override IApplyData __dataIn(QVoid data) => data;
        public override IApplyData __dataOut(QVoid data) => data;
        public static System.Threading.Tasks.Task<QVoid> Run(IOperationFactory __m__)
        {
            return __m__.Run<HelloQ, QVoid, QVoid>(QVoid.Instance);
        }
    }
}