print "--shell pipeline sugar--";
out = shellpipe { "echo" "-e" "apple\nbanana\napple\norange\nbanana\napple" | "sort" | "uniq" "-c" | "sort" "-nr" };
print out.stdout;

// equals as
print "--shell pipeline desugar--";
seq {
    out = shell { "echo", ["-e", "apple\nbanana\napple\norange\nbanana\napple"] };
    out = shell { "sort", [], out.stdout };
    out = shell { "uniq", ["-c"], out.stdout };
    out = shell { "sort", ["-nr"], out.stdout };
}

print out.stdout;

// equals as following one expression statement
// this can be used as the direct desugar of the pipeline
print "--shell pipeline further desugar--";
seq {
    // outer most
    print (shell { 
        "sort", 
        ["-nr"], 
        // 3rd inner
        (shell { 
            "uniq", 
            ["-c"], 
            // 2nd inner
            (shell { 
                "sort", 
                [], 
                // 1st inner
                (shell { 
                    "echo", 
                    ["-e", "apple\nbanana\napple\norange\nbanana\napple"] 
                }).stdout
            }).stdout 
        }).stdout 
    }).stdout;
}

