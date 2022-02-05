# SimPyTest: Test case generation for simple Python programs

## Input form

For the function themselves:

- simple function that is ok as long as they don't throw an exception
- simple function and validator function, the output of the first is the input of the second,
  try to make the second function return false
- tableaux d' actions et un object affecté par ces actions => into verif or no exception
- liste de set d'actions

For the parameters
- register all the parameters
  - set domain (optional)
  - set additional corner case (default ste for each primitive type)
- auto-detect the parameter list and detect the domain and the basic corner case.
  - some corner case could be extended using fuzzing, symbolic execution, etc

## Techniques of testing
### Blackbox

- Fuzzing I/O
- Property based testing ( nice python implem: [https://hypothesis.works/](hypothesis.works/) )
- Partitioning testing

### Whitebox

- Fault injection (variant of fuzzing)
- Symbolic execution
  - Concolic testing (degraded symbolic execution)


## Notes
All the challenge will be in determining the domain of the input

=> When a failing test is discovered for a student, save it on the student profile / for all the tests ?

## TODO

- Create an error recorder ?  

- fuzzy step testing
  - protect against code running for too long 
  - add the support for parameter in the steps searching
  - add a form of A* optimization / alpha beta pruning
- all the missing testing type
