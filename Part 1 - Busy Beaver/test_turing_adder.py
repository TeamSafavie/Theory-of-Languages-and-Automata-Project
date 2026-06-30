from turing_machine import TuringMachine

def print_states(transition_mapping):
    states = set()
    for (start, finish) in transition_mapping.items():
        (s1, _) = start
        (s2, _, _) = finish
        states.add(s1)
        states.add(s2)
    print("The Turing machine has", len(states), "states:")
    for i in states:
        print(i)
    print()

transitions = {
    ('q0', '1'): ('q0', '1', 'R'),

    ('q0', '0'): ('q1', '1', 'R'),

    ('q1', '1'): ('q1', '1', 'R'),

    ('q1', ''): ('q2', '', 'L'),
    ('q2', '1'): ('qa', '', 'R')
}

if __name__ == "__main__":
    print_states(transitions)
    machine = TuringMachine(transitions)

    def run(input_):
        w = input_
        print("Input:",w)
        print("Accepted" if machine.accepts(w) else "Rejected")
        machine.debug(w)
        print()

    run("110111")
    run("11101111")
    run("0111")