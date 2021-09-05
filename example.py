from cfg_string_gen import cfg_string_generator, RepetitionMode

rules = {'S': ['0A', '1B'], 'A': ['0AA', '1S', '1'], 'B': ['1BB', '0S', '0']}
depth = 6

new_line = '\n'

print('Strings:')
strings = cfg_string_generator(rules, depth, derivation=False, repetition=RepetitionMode.enabled, low_memory=False)
[print(x) for x in strings]
print('')

print('With derivations, without nonterminal index:')
derivations1 = cfg_string_generator(rules, depth, derivation=True, repetition=RepetitionMode.enabled, low_memory=True)
[print(f'{k} ->\n{new_line.join(", ".join(str(t) for t in d) for d in v)}\n') for k, v in derivations1.items()]
print('')

print('With one derivation per string:')
derivations2 = cfg_string_generator(rules, depth, derivation=True, repetition=RepetitionMode.disabled, low_memory=False)
[print(f'{k} ->\n{new_line.join(", ".join(str(t) for t in d) for d in v)}\n') for k, v in derivations2.items()]
print('')

print('Strings with count:')
count_strings = cfg_string_generator(rules, depth, derivation=False, repetition=RepetitionMode.count, low_memory=False)
[print(f'{x} -> {y}') for x, y in count_strings.items()]
print('')
