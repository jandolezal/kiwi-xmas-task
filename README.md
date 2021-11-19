# Solution to Python weekend entry task

Solution for the entry task assignment for Python weekend in Prague, 10 – 12 December 2021.

The solution is in one module `solution.py` and should work in Python >=3.7.

From the additional options, `--bags` is implemented.

## Usage

`python3 -m solution -h`

```
usage: kiwi-xmas-task [-h] [-b BAGS] filename origin destination

finds all possible routes between origin and destination based on the number of
bags.

positional arguments:
  filename              specify name of a CSV file which contains flights
                        data.
  origin                set origin (three letter code)
  destination           set destination (three letter code)

optional arguments:
  -h, --help            show this help message and exit
  -b BAGS, --bags BAGS  set number of bags (default: 0)
```

Example usage with one of the provided flights dataset.

`python3 -m solution example0.csv WIW ECV --bags=1`


## Test

There are only few tests covering couple of helper functions, but not the main logic of finding the routes.

`python3 -m unittest test_solution.py`
