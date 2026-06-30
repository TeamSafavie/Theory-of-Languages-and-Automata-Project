# -*- coding: utf-8 -*-
"""A Turing machine simulator skeleton.

    Accepting '#'
    =============

    >>> from turing_machine import TuringMachine

    Instantiate the machine with particular transitions.

    >>> one_hash = TuringMachine(
    ...     {
    ...         ('q0', '#'): ('saw_#', '#', 'R'),
    ...         ('saw_#', ''): ('qa', '', 'R'),
    ...     }
    ... )

    Check whether it accepts a string:

    >>> one_hash.accepts('#')
    True

    >>> one_hash.accepts('##')
    False

    Check whether it rejects a string:

    >>> one_hash.rejects('#')
    False

    >>> one_hash.rejects('##')
    True
"""

import logging

class TuringMachine:
    """Turing machine simulator class.

    A machine is instantiated with transitions, start, accept and reject states
    and a blank symbol. We assume that the input and the tape alphabet can be
    deducted from the transitions.

    :param dict transitions: a mapping from (state, symbol) tuples to (state,
    symbol, direction) tuple. Directions are either 'L' (for left) or 'R' (for right).

    :param start_state: the initial state of the machine.

    :param accept_state: the accept state.

    :param reject_state: the reject state.

    :blank_symbol: the special symbol that marks the tape cell to be empty.

    """

    def __init__(self, transitions, start_state='q0', accept_state='qa', reject_state='qr', blank_symbol='', finite=False):
        self.transitions = transitions
        self.start_state = start_state
        self.accept_state = accept_state
        self.reject_state = reject_state
        self.blank_symbol = blank_symbol
        self.finite = finite

    def run(self, input_):
        """Execute the Turing machine for a particular input.

        :param input_: the input that is written on the tape. It can be a list
        of strings, or just a string, in which case each letter is treated as a symbol.

        This method MUST be a Python generator. It should yield a (action, configuration) tuple
        at each step of the computation.
        
        The action is either 'Accept', 'Reject' or None. 
        
        Configuration is a dictionary with the following keys:
        - 'state': the current state,
        - 'left_hand_side': list of symbols on the left hand side of the current position (closest first),
        - 'symbol': the current symbol under the head,
        - 'right_hand_side': list of symbols on the right hand side of the current position.

        """
        if isinstance(input_, str):
            tape = list(input_) if input_ else [self.blank_symbol]
        else:
            tape = list(input_) if input_ else [self.blank_symbol]
            
        head_pos = 0
        state = self.start_state
        
        while True:

            if not tape:
                tape = [self.blank_symbol]
                head_pos = 0
                
            lhs = tape[:head_pos]
            symbol = tape[head_pos]
            rhs = tape[head_pos+1:]
            
            config = {
                'state': state,
                'left_hand_side': lhs,
                'symbol': symbol,
                'right_hand_side': rhs
            }
            
            action = None
            if state == self.accept_state:
                action = 'Accept'
            elif state == self.reject_state:
                action = 'Reject'
                
            yield (action, config)
            
            if action is not None:
                break
                
            if (state, symbol) in self.transitions:
                next_state, write_symbol, direction = self.transitions[(state, symbol)]
            else:
                yield ('Reject', config)
                break
                
            tape[head_pos] = write_symbol
            state = next_state
            
            if direction == 'R':
                head_pos += 1
                if head_pos >= len(tape):
                    tape.append(self.blank_symbol)
            elif direction == 'L':
                head_pos -= 1
                if head_pos < 0:
                    if self.finite:
                        logging.warning("Crossed left boundary on finite/singly-infinite tape.")
                    tape.insert(0, self.blank_symbol)
                    head_pos = 0

    def accepts(self, input_, step_limit=100):
        """Check whether the Turing machine accepts a string.

        :param input_: the input string or list.
        :param step_limit: the maximum number of steps to simulate before stopping.
        :return: True if the machine halts in accept_state, False if it rejects,
                 or None if the step limit is reached without halting.
        """
        gen = self.run(input_)
        for i, (action, config) in enumerate(gen):
            if action == 'Accept':
                return True
            elif action == 'Reject':
                return False
            
            if i >= step_limit:
                logging.warning(f"Step limit {step_limit} reached without halting.")
                return None
        return None

    def rejects(self, input_, **kwargs):
        """Check whether the Turing machine rejects a string.

        :param input_: the input string or list.
        :return: True if the machine rejects the string, False if it accepts.
        """
        res = self.accepts(input_, **kwargs)
        if res is None:
            return None
        return not res

    def debug(self, input_, step_limit=100, colored=True):
        """Print the execution configuration of the machine per transition for debugging.

        :param input_: the input string or list.
        :param step_limit: the maximum number of steps to output.
        :param colored: True to output colored boundaries in terminal.
        """
        gen = self.run(input_)
        for i, (action, config) in enumerate(gen):
            lhs = "".join(config['left_hand_side'])
            sym = config['symbol']
            rhs = "".join(config['right_hand_side'])
            state = config['state']
            
            if colored:
                print(f"{state:15} {lhs}\033[91m[{sym}]\033[0m{rhs}")
            else:
                print(f"{state:15} {lhs}[{sym}]{rhs}")
                
            if action is not None:
                break
                
            if i >= step_limit:
                print(f"Step limit {step_limit} reached.")
                break