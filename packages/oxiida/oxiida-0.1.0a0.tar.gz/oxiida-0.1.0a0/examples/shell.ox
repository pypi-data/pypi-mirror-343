seq {
    out1 = shell {"echo", ["-n", "thanks rust!"]};
    out2 = shell {"echo", ["-n", "thanks rust!", out1.stdout]};

    print "---stdout---";
    print out2.stdout;
    print "---stderr---";
    print out2.stderr;
    print "---status---";
    print out2.status;
}

print "---stdout---";
print (shell {"ls"}).stdout;

print "---stdout---";
print (shell {"ls", []}).stdout;
