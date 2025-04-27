// two seq blocks are supposed to run at the "same" time
para {
    print "-- anchor --";
    print (shell {"date", ["+%S, %N"]}).stdout;
    seq {
        shell {"sleep", ["2"]};
        print "1st: " + (shell {"date", ["+%S, %N"]}).stdout;
    }

    seq {
        shell {"sleep", ["2"]};
        print "1st: " + (shell {"date", ["+%S, %N"]}).stdout;
    }
}

// as comparison run in sequence
seq {
    print "-- anchor --";
    print (shell {"date", ["+%S, %N"]}).stdout;
    seq {
        shell {"sleep", ["2"]};
        print "2nd: " + (shell {"date", ["+%S, %N"]}).stdout;
    }

    seq {
        shell {"sleep", ["2"]};
        print "2nd: " + (shell {"date", ["+%S, %N"]}).stdout;
    }
}
