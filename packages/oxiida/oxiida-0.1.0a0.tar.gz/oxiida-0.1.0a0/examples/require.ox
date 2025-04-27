require py_plus;
require time, sleep;

para {
    print "--anchor--";
    print time();
    seq {
        sleep(2);
        print time();
    }

    seq {
        sleep(2);
        print time();
    }
}

seq {
    print "--anchor--";
    print time();
    seq {
        sleep(2);
        print time();
    }

    seq {
        sleep(2);
        print time();
    }
}

y = 7;
print py_plus(10, y);
