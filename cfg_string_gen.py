from cfg_queues import *
import re


class Detail:
    @staticmethod
    def string_gen(rules, depth, out, insert_function, queue):
        # used to search for nonterminals in strings
        regex = re.compile('|'.join([f'({x})' for x in rules]))
        queue.put('S')  # starting nonterminal

        stop_gate = -1  # used to separate depths apart
        for i in range(depth, -1, -1):
            queue.put(stop_gate)
            while True:
                s = queue.take()
                if type(s) is int:
                    # all this depth's strings have been generated
                    break
                match = regex.search(s)
                if match is None:
                    # string generated
                    insert_function(out, s)
                    continue
                # derivate with all possibilities
                for sub in rules[match.group()]:
                    queue.put(s[:match.start()] + sub + s[match.end():])

        # get the last strings generated
        while not queue.empty():
            s = queue.take()
            match = regex.search(s)
            if match is None:
                insert_function(out, s)
        return out

    @staticmethod
    def derivation_gen(rules, depth, low_memory, out, insert_function, queue):
        # if low_memory is true, don't include de position of the non terminal on the derivation list
        derivation_init = (lambda pos, der: der) if low_memory else (lambda pos, der: (pos, der))
        # used to search for nonterminals in strings
        regex = re.compile('|'.join([f'({x})' for x in rules]))
        queue.put(('S', [[]]))  # starting nonterminal

        while not queue.empty():
            s = queue.take()
            match = regex.search(s[0])
            if match is None:
                # string generated
                insert_function(out, s)
                continue
            # filter for derivations that aren't deeper than depth
            available_derivations = [x for x in s[1] if len(x) < depth]
            if len(available_derivations) == 0:
                # this string still has nonterminals and it reached max depth
                continue
            # derivate with all possibilities
            for sub in rules[match.group()]:
                new_string = s[0][:match.start()] + sub + s[0][match.end():]
                derivations = [x + [derivation_init(match.start(), sub)] for x in available_derivations]
                queue.put((new_string, derivations))
        return out


class RepetitionMode:
    disabled = 0
    enabled = 1
    count = 2


def cfg_string_generator(rules, max_depth, derivation=False, repetition=RepetitionMode.disabled, low_memory=False):
    """"generates strings of a context free grammar until a certain depth
    rules: a dict with de derivation rules of the context free grammar
    max_depth: the maximum number of derivations for a string to generate (controls memory usage)
    derivation: enables derivation storage
    repetition: enables storage of repetitions
    low_memory: enables not including nonterminal position on derivations"""
    if derivation:
        def inserter(d, v):
            d[v[0]] = v[1]

        return Detail.derivation_gen(rules, max_depth, low_memory, {}, inserter,
                                     AdditiveDictQueue() if repetition else ConservativeDictQueue())
    else:
        if repetition == RepetitionMode.count:
            def inserter(s, v):
                s.insert(v)

            count = Detail.string_gen(rules, max_depth, CountSet(), inserter, SetQueue(CountSet()))
            return count.dict
        else:
            if repetition:
                def inserter(list_, value):
                    list_.append(value)

                return Detail.string_gen(rules, max_depth, [], inserter, Queue())
            else:
                def inserter(set_, value):
                    set_.add(value)

                return Detail.string_gen(rules, max_depth, set(), inserter, SetQueue(set()))


def main():
    print('Called as main, getting grammar from user input')
    rules = {}
    while True:
        nonterminal = input('Input a nonterminal. Type nothing to proceed ')
        if len(nonterminal) == 0:
            break
        derivations = input('Type the derivation rules separated by commas:\n').rstrip().split(',')
        rules[nonterminal] = derivations
        print('')

    if 'S' not in rules:
        print('No starting nonterminal \'S\'!')
        exit()

    derivation_in = input('Store derivation steps with the strings? (Y/N, default: N) ').rstrip()
    derivation = derivation_in == 'Y' or derivation_in == 'y'

    if derivation:
        low_mem_in = input(
            'Store the position of the nonterminal with the derivation steps? Doing so uses more memory (Y/N, '
            'default: N) ').rstrip()
        low_mem = not (low_mem_in == 'Y' or low_mem_in == 'y')
    else:
        low_mem = False  # doesn't make a difference

    if derivation:
        repetition_in = input('How to store string repetitions? (N)o storing, (S)tore all (default: N) ').rstrip()
    else:
        repetition_in = input(
            'How to store string repetitions? (N)o storing, (S)tore all, (C)ount occurrences (default: N) ').rstrip()
    if repetition_in == 'S':
        repetition = RepetitionMode.enabled
    elif repetition_in == 'C':
        repetition = RepetitionMode.count
    else:
        repetition = RepetitionMode.disabled

    max_depth_in = input(
        'Max number of derivations for a string. Warning: Put a number too high and memory usage will explode ('
        'default: 6) ')
    try:
        max_depth = int(max_depth_in)
    except ValueError:
        max_depth = 6

    result = cfg_string_generator(rules, max_depth, derivation, repetition, low_mem)

    new_line = '\n'
    if derivation:
        [print(f'{k} ->\n{new_line.join(", ".join(str(t) for t in d) for d in v)}\n') for k, v in result.items()]
    else:
        if repetition == RepetitionMode.count:
            [print(f'{x} -> {y}') for x, y in result.items()]
        else:
            [print(x) for x in result]


if __name__ == '__main__':
    main()
