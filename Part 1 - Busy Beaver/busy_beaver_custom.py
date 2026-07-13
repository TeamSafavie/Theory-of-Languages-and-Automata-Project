import sys

class Error(Exception):
    pass

class TuringMachine(object):
    def __init__(self, program, start, halt, init):
        self.program = program
        self.start = start
        self.halt = halt
        self.init = init
        self.tape = [self.init]
        self.pos = 0
        self.state = self.start
        self.set_tape_callback(None)
        self.tape_changed = 1
        self.movez = 0

    def run(self):
        tape_callback = self.get_tape_callback()
        while self.state != self.halt:
            if tape_callback:
                tape_callback(self.tape, self.tape_changed)

            lhs = self.get_lhs()
            rhs = self.get_rhs(lhs)

            new_state, new_symbol, move = rhs

            old_symbol = lhs[1]
            self.update_tape(old_symbol, new_symbol)
            self.update_state(new_state)
            self.move_head(move)

        if tape_callback:
            tape_callback(self.tape, self.tape_changed)

    def set_tape_callback(self, fn):
        self.tape_callback = fn

    def get_tape_callback(self):
        return self.tape_callback

    property(get_tape_callback, set_tape_callback)

    @property
    def moves(self):
        return self.movez

    def update_tape(self, old_symbol, new_symbol):
        if old_symbol != new_symbol:
            self.tape[self.pos] = new_symbol
            self.tape_changed += 1
        else:
            self.tape_changed = 0

    def update_state(self, state):
        self.state = state

    def get_lhs(self):
        under_cursor = self.tape[self.pos]
        lhs = self.state + under_cursor
        return lhs

    def get_rhs(self, lhs):
        if lhs not in self.program:
            raise Error('Could not find transition for state "%s".' % lhs)
        return self.program[lhs]

    def move_head(self, move):
        if move == 'l':
            self.pos -= 1
        elif move == 'r':
            self.pos += 1
        else:
            raise Error('Unknown move "%s". It can only be left or right.' % move)

        if self.pos < 0:
            self.tape.insert(0, self.init)
            self.pos = 0
        if self.pos >= len(self.tape):
            self.tape.append(self.init)

        self.movez += 1

beaver_programs = [
    { },
    {
        'a0': ('h', '1', 'r'),
        'a1': ('h', '1', 'r'),
    },
    {
    'a0': ('b', '1', 'r'),
    'a1': ('h', '1', 'r'),
    'b0': ('b', '1', 'l'),
    'b1': ('a', '1', 'l'),
    },
    {
    'a0': ('b', '1', 'r'),
    'a1': ('h', '1', 'r'),
    'b0': ('b', '1', 'l'),
    'b1': ('c', '0', 'r'),
    'c0': ('c', '1', 'l'),
    'c1': ('a', '1', 'l'),
    },
    {
    'a0': ('b', '1', 'r'),
    'a1': ('a', '0', 'l'),
    'b0': ('c', '1', 'r'),
    'b1': ('b', '1', 'l'),
    'c0': ('b', '1', 'l'),
    'c1': ('d', '1', 'r'),
    'd0': ('h', '1', 'r'),
    'd1': ('a', '0', 'r'),
    },
    {
    'a0': ('b', '1', 'r'),
    'a1': ('a', '1', 'l'),
    'b0': ('c', '1', 'r'),
    'b1': ('e', '1', 'l'),
    'c0': ('d', '1', 'r'),
    'c1': ('e', '1', 'r'),
    'd0': ('a', '0', 'l'),
    'd1': ('c', '1', 'r'),
    'e0': ('h', '1', 'r'),
    'e1': ('b', '0', 'l'),
    },
    { # current champion, found by mxdys, producing 2 ^ 65536 '1's on the tape. this machine always halts,
      # and currently holds the record, but is not yet proven to be the best machine in terms of the number of "1"s.  
    'a0': ('b', '1', 'r'),
    'a1': ('a', '1', 'r'),
    'b0': ('c', '1', 'r'),
    'b1': ('h', '1', 'r'),  
    'c0': ('d', '1', 'l'),
    'c1': ('f', '0', 'r'),
    'd0': ('a', '1', 'r'),
    'd1': ('e', '0', 'l'),
    'e0': ('d', '0', 'l'),
    'e1': ('c', '1', 'r'),
    'f0': ('a', '1', 'r'),
    'f1': ('e', '0', 'r'),
    }
]

def busy_beaver(n):
    def tape_callback(tape, tape_changed):
        if tape_changed:
            print(''.join(tape))

    program = beaver_programs[n]

    print("Running Busy Beaver with %d states." % n)
    tm = TuringMachine(program, 'a', 'h', '0')
    tm.set_tape_callback(tape_callback)
    tm.run()
    number_of_ones_generated = tm.tape.count('1')
    print("Busy beaver finished in %d steps." % tm.moves)
    print(f"Busy beaver generated {number_of_ones_generated} ones!")

def usage():
    print("Usage: %s [1|2|3|4|5|6]" % sys.argv[0])
    print("Runs Busy Beaver problem for 1 or 2 or 3 or 4 or 5 or 6 states.")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            n = int(sys.argv[1])
        except ValueError:
            usage()
    else:
        try:
            user_input = input("Enter the number of states to run (1, 2, 3, 4, or 5): ")
            n = int(user_input)
        except ValueError:
            print("Invalid input! Please enter a number.")
            sys.exit(1)

    if n < 1 or n > 5:
        print("Error: 'n' must be between 1 and 5 inclusive.")
        sys.exit(1)

    busy_beaver(n)