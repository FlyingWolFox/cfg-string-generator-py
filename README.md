# cfg-string-generator

A library that generates strings for context free grammars.
A python port of [cfg-string-generator](https://github.com/FlyingWolFox/cfg-string-generator) with a user input grammar as extra

## How to use

To get a container with the derivations call:

```python
def cfg_string_generator(rules, max_depth, derivation=False, repetition=RepetitionMode.disabled, low_memory=False):
```

The template parameters modify the behavior of the generator as follows:

* `derivation`: enables storage of derivations. If disabled, a simple container containing generated strings will be returned, if enabled, a `std::unordered_map` will be returned, containing the the generated string as keys and a `std::vector` containing string derivations. Default is `false`
* `repetition`: dictates how the generator should handle repeated string (happens on ambiguous grammars). Use a `cfg_string_gen::repetition_mode` here. Possible values are:
  * `repetition_mode::disabled` (aka `0`): repetitions won't be recorded. If `derivation` is false, this'll make the function return a `std::unordered_set` of strings, if not, each string on the map will have only one derivation (the first one to have generated the string)
  * `repetition_mode::enabled` (aka `1`): repetitions will be recorded. If `derivation` is false, a `std::vector` will be returned containing all strings, if not, each string on the map will have all possible derivations
  * `repetition_mode::count` (aka `2`): count the number of repetitions. This'll have effect only if `derivation` is `false`, if not behavior is equal of `repetition_mode::enabled`. Returns a `std::unordered_map` containing the strings as keys and the number of occurrences as values
* `low_memory`: controls if derivations should also store the position of the nonterminal (redundant information). If `true` these positions aren't stored. The memory impact of this depends on the grammar
* `RulesMap`: the type of the rules parameter, which should be a map type like `std::map`. Should be deducted from the function parameters

The parameters are as follows:

* `rules`: a dict containing the context free grammar rules. The keys should be the nonterminals and the values a list with the rules. Nonterminals are expected to be a single char, and the nonterminal 'S' must be present
* `max_depth`: the max depth which the generator should go. Since the generation has exponential behavior and grammars may generate infinite languages, this controls memory usage. A depth of 0 means no derivation has been made, and a depth of 1 means all possible rules were applied with the leftmost nonterminal
* `derivation`: enables storage of derivations. If disabled, a simple container containing generated strings will be returned, if enabled, a `dict` will be returned, containing the the generated string as keys and a `list` containing string derivations. Default is `false`
* `repetition`: dictates how the generator should handle repeated string (happens on ambiguous grammars). Use a `cfg_string_gen.RepetitionMode` here. Possible values are:
  * `RepetitionMode.disabled` (aka `0`): repetitions won't be recorded. If `derivation` is false, this'll make the function return a `set` of strings, if not, each string on the map will have only one derivation (the first one to have generated the string)
  * `RepetitionMode.enabled` (aka `1`): repetitions will be recorded. If `derivation` is false, a `list` will be returned containing all strings, if not, each string on the map will have all possible derivations
  * `RepetitionMode.count` (aka `2`): count the number of repetitions. This'll have effect only if `derivation` is `false`, if not behavior is equal of `RepetitionMode.enabled`. Returns a `dict` containing the strings as keys and the number of occurrences as values
* `low_memory`: controls if derivations should also store the position of the nonterminal (redundant information). If `true` these positions aren't stored. The memory impact of this depends on the grammar

There's usage examples in `example.py`

## Return values and structures

The return type of the generator depends on the template parameters, they will be:

* `list`: Contains all generated strings in some order. The primary ordering is the number of derivations necessary to generate the string an the secondary is dependent on the ordering of the nonterminals on the rules map. Returned when `derivation` is `false` and `repetition` is `RepetitionMode.enabled`
* `set`: Contains all generated strings without repetitions. Returned when `derivation` is `false` and `repetition` is `RepetitionMode.disabled`
* `dict(string, int)`: Contains all generated strings with a occurrence count. Returned when `derivation` is `false` and `repetition` is `RepetitionMode.count`
* `dict(string, list(list(tuple(int, string))))`: Contains strings and it's derivations. The list of tuples is a single derivation. The first item of tuple is the position of the nonterminal replaced, and the second item is the substitution made. Returned when `derivation` is `true` and `low_memory` is `false`
* `dict(string, list(list(string)))`: Contains strings and it's derivations. The list of strings is a single derivation. Returned when `derivation` is `true` and `low_memory` is `true`

## Warning

Due to the exponential nature of string generation this will use a **lot** of memory, use with caution, controlling the `max_depth`. Ways to get minimum memory usage:

* Enable storage of derivations just when needed
* Consider enabling `low_memory`. In simpler grammars the effect of this is noticeable (see one in the example directory)
* Enable repetition storage just when needed, both for derivation storage or not. In ambiguous grammars this'll save a lot of memory
* If you need repetitions in just string generation, consider using `RepetitionMode.count`. It gives the occurrence number and saves memory

Of course all memory saving measures may affect performance, mostly a small bit.

However **always** take care of `max_depth` value. Just an increment may increase memory usage by a lot (manly when repetitions are being stored)

## Contributing

Any performance, functionality and memory consumption improvements are welcome. Bug reports and documentation improvements are also welcome
