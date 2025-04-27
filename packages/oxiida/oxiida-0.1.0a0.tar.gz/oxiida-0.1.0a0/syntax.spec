// lex the workflow language
// In rust it can use macro to define.
// here is more for a generic DSL defined from scratch with a concret specification.
// The input has raw format with also the ShellProcess definition in it.

// simple seq operation
// wf foobar(input: I) -> OB {
//     proc proc_a = AProcess[I -> OA]
//     proc proc_b = BProcess[OA -> OB]
//     
//     out_a = proc_a(input)
//     out = proc_b(out_a)
//
//     return out
// }

// seq with data modification
// type should be restrictly respected
// wf foobr(input: I) -> OB {
//     proc proc_a = AProcess[I -> OA]
//     proc proc_b = BProcess[O_M -> OB]
//     
//     out_a = proc_a(input)
//     om = O_M {
//         field1: out_a.x0,
//         field2: out_a.x2,
//     }
//     out = proc_b(om)
//
//     return out
// }

// simple seq with multiple inp/out
// wf foobar(inp1: I1, inp2: I2, inp3: I3) -> OC1, OB2 {
//     proc proc_a = AProcess[I1, I2 -> OA]
//     proc proc_b = BProcess[I2, I3 -> OB1, OB2]
//     proc proc_c = CProcess[OA, OB1 -> OC1, OC2]
//     
//     out_a = proc_a(inp1, inp2)
//     out_b1, out_b2 = proc_b(inp2, inp3)
//     out_c1, out_c2 = proc_c(out_a, outb1)
//
//     return out_c1, outb2
// }

// parallel with async like syntax
// wf foobar(inp: I) -> OC {
//     proc proc_a = AProcess[I -> OA]
//     proc proc_b = BProcess[I -> OB]
//     proc proc_c = CProcess[OA, OB -> OC]
//
//     // non-blocking
//     // ox: is to launch proc in parallel, think about `go` in Golang
//     fut_a = ox proc_a(inp)
//     fut_b = ox proc_b(inp)
//
//     // wait until both are finished
//     out_a = wait fut_a
//     out_b = wait fut_b
//
//     // syntax error if any fut is not wait, which means resource leak
//     return proc_c(out_a, out_b)  
// }

// if..else conditional operation
// wf foobar(input: I) -> O {
//     proc proc_t = TrueProcess[I -> O]
//     proc proc_f = FalseProcess[I -> O]
//
//     // define here to respect the scope of condition
//     condition = input.check
//
//     if (condition) {
//         // change condition inside is a compile time error, violate the lifetime rule
//         out = proc_t(input)
//     } else {
//         out = proc_f(input)
//     }
//
//     return out
// }

// // while loop operation
// wf foobar(input: I) -> O {
//     proc proc_loop_inner = LoopProcess[I -> I]
//     proc proc_final = FinalProcess[I -> O]
//
//     curr = I_sub {
//         field0: input.x0
//     }
//
//     while (curr.field0 < 10) {
//         iout = proc_loop_inner(curr)
//         curr = I_sub {
//             field0: iout.x0
//         }
//     }
//
//     return proc_final(curr)
// }
//
// // for
// wf foobar(input: I) -> O {
//     proc proc_for_inner = ForInnerProcess[IN -> IN]
//     proc proc_final = FinalProcess[I -> O]
//
//     curr = I_sub {
//         field0: input.x0
//     }
//
//     for (i in input.loop_idx) {
//         iout = proc_loop_inner(curr)
//         curr = I_sub {
//             field0: iout.x0
//         }
//     }
//
//     return proc_final(curr)
// }

// for
wf foobar(input: I) -> O {
    proc proc_for_inner = ForInnerProcess[IN -> IN]
    proc proc_final = FinalProcess[I -> O]

    wg wg1 = WaitGroup

    for (i in input.loop_idx) {
        inp = IN {
            field0: input.x0 + i
        } 
        // or any process that convert I -> IN

        fut_iout = ox proc_loop_inner(inp)
        wg1.push(fut_iout)
    }

    // ??? it has to be a vec like type, really needed???
    resolved = wait wg1
    curr = I {
        field0: resolved[0],
        field1: resolved[1],
        field2: resolved[2],
    }
    // or any process that convert vec[IN] -> I
    return proc_final(curr)
}


// sequential shell tasks
seq {
    output = shell@localhost {"echo", "thanks rust!"};
    res = shell@localhost {"echo", output.stdout};

    return res;
}

// parallel execution
para {
    stmt1
    stmt2
}

// mixture seq/para
seq {
    stmt1
    stmt2
    para {
        stmt3
        stmt4
    }
}

// seq/para while, default while is seq while
para while(i < 10) {
    stmt4
    i = i + 1;
}
