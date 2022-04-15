# SimPyTest: Test case generation for simple Python programs

[https://snail.info.unamur.be/project/msc-pierre-ortegat/](Page unamur)

## Input form

For the function themselves:

- simple function that is ok as long as they don't throw an exception
- simple function and validator function, the output of the first is the input of the second, try to make the second
  function return false
- tableaux d' actions et un object affecté par ces actions => into verif or no exception
- liste de set d'actions

For the parameters

- register all the parameters
    - set domain (optional)
    - set additional corner case (default ste for each primitive type)
- auto-detect the parameter list and detect the domain and the basic corner case.
    - some corner case could be extended using fuzzing, symbolic execution, etc

## Techniques of testing

- Search based testing: [https://link.springer.com/chapter/10.1007/978-3-030-59762-7_2](springer)

### Blackbox

- Fuzzing I/O [https://www.fuzzingbook.org](www.fuzzingbook.org)
- Property based testing ( nice python implem: [https://hypothesis.works/](hypothesis.works/) )
- Partitioning testing

### Whitebox

- Fault injection (variant of fuzzing)
- Symbolic execution
    - Concolic testing (degraded symbolic execution)

## Done

### Step combination testing

see: StepsRunner.py

### Symbolic execution / Concolic testing

https://docs.python.org/3/library/ast.html

input : function name to test + src file path

idea: parse the code and load the vars into a constraint solver to get all branch possible results

https://pypi.org/project/python-constraint/

1 - parse the ast to define for each new branch the condition needed to get there 2 - remove as much as possible less
precise condition (eg: a > 3 and a > 3 && b < 2; the second one will always trigger the first one). DON'T remove the
first one if the second one is not solvable.

return condition and unateignable branchs

TODO:

- ajouter un regisrte à constantes
- filtrer les contextes intéressants à la fin: pas besoin d'avoir les ctx des popotes internes au branche si elles
  n'amenent nulle part
- limiter profondeur
- mechanisme anti boucles / recursion

IMPORTNANT !!! : résolution des condition des boucles est IMPOSSBILE ! Voir "Halting problem" en cs Une simplification
et approche limitée est la seule solution possible. Ou bien execution simplifiée controlée ?

Note importante bis: le parse python optimise le code: aka les stments inutiles seront virés sans wanr

### Partition testing

TODO

### Property based testing

TODO

### Fuzzing

en cours, check fuzezing module

TODO check pour le timeout

### Fault injection

TODO

## Notes

All the challenge will be in determining the domain of the input

=> When a failing test is discovered for a student, save it on the student profile / for all the tests ?

## TODO

- static parsing of the code to find magic token
  - [x] done in magic_token_finder, now integrate that into the fuzzer 
  - [x] resolve the method to follow them
  - [x] manage module scoping for the function resolution
  - [ ] resolve static expression to find more magic token

- [x] add bool type

- [x] add args detection to the fuzzer (annotation)

- [ ] create a basic inginous integration [link](https://docs.inginious.org/en/v0.7/admin_doc/install_doc/installation.html#installing-inginious)
  - [x] of the fuzzer with a checker function
  - [ ] of the fuzzer without reference code
  - [x] of the combiner with some reference code
  - [ ] of the combiner without reference code

- [x] combiner add nice_name

- [ ] make a simplified interface

- [ ] add a stop after one fail option to the fuzzer

- [x] combiner compare the output also

- [ ] combiner allow no ref fn mode

- [ ] combiner add allowed errors

- [ ] combiner add option to only report the exception of the tested code

- [ ] add a global and per-run timeout

- [ ] combiner add controlled entropy sources

- [ ] combine the fuzzer and the combination of steps

- [ ] edit the runner in a way that allow to just pass a function (moar syntaxic sugar :D )

- [ ] add time limit

- ajouter un fuzzer qui teste par lignes "hot" et "cold" (aka, si une seed passe sur une ligne qu'on n'execute
  jamais, elle ramassera pas mal de points)

- all the missing testing type

- add args detection to the fuzzer (dynamic detection)

- fuzzy step testing
    - add a mex global depth
    - add the support for parameter in the steps searching
    - add a form of A* optimization / alpha beta pruning
    - 
- state comparer (compare les embriquement de classes entre le code exemple et le code élève)

- checkout comment créer des profils de tests pour que une entrée qui aie cassé le code d'un étudiant soie restée sans
  devoir la rechercher avant de relancer le process

- checkout fault injection
- checkout partition testing
- checkout property base testing
- checkout concolic testing
- checkout symbolic execution
