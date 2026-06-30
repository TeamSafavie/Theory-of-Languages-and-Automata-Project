from turing_machine import TuringMachine
from test_turing_machine_example1 import print_states

transitions = {
    ('q0', '1'): ('q1', 'X', 'R'),
    ('q0', '0'): ('q5', 'M', 'L'),

    ('q1', '1'): ('q1', '1', 'R'),
    ('q1', '0'): ('q2', '0', 'R'),

    ('q2', '1'): ('q3', 'Y', 'R'),
    ('q2', 'Y'): ('q2', 'Y', 'R'),
    ('q2', 'Z'): ('q2', 'Z', 'R'),
    ('q2', ''): ('q7', '', 'L'),

    ('q3', '1'): ('q3', '1', 'R'),
    ('q3', 'Z'): ('q3', 'Z', 'R'),
    ('q3', ''): ('q4', 'Z', 'L'),

    ('q4', 'Z'): ('q4', 'Z', 'L'),
    ('q4', '1'): ('q4', '1', 'L'),
    ('q4', 'Y'): ('q2', 'Y', 'R'),

    ('q5', 'X'): ('q5', '', 'L'),
    ('q5', ''): ('q8', '', 'R'),

    ('q6', '1'): ('q6', '1', 'L'),
    ('q6', 'X'): ('q0', 'X', 'R'),

    ('q7', 'Z'): ('q7', 'Z', 'L'),
    ('q7', 'Y'): ('q7', '1', 'L'),
    ('q7', '0'): ('q6', '0', 'L'),
    
    ('q8', ''): ('q8', '', 'R'),
    ('q8', 'M'): ('q9', '', 'R'),
    
    ('q9', '1'): ('q9', '', 'R'),
    ('q9', 'Z'): ('q9', '1', 'R'),
    ('q9', ''): ('qa', '', 'L'),
}

if __name__ == "__main__":
    print_states(transitions)
    machine = TuringMachine(transitions)

    def run(input_):
        w = input_
        print("Input:", w)
        print("Accepted" if machine.accepts(w) else "Rejected")
        machine.debug(w, step_limit=2500)
        print()

    run("110111") #Accept 111111
    run("11101111") #Accept 111111111111
    run("01111") #Accept 0
