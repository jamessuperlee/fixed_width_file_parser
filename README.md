# Fixed Width File Parser Application

This is an application which enables for a user to generate a csv file by parsing a fixed width file with spec. The input will be a input file path and a spec file path.


## Environment
* Python3.8
* test framework - pytest


## How to run lint and test

```bash
$ ./scripts/test.sh
```


## How to run a tool
```bash
./scripts/run.sh --input-file ./sample_data/fwf.txt --spec-file ./sample_data/spec.json
```
After you successfully run this tool, you can see a output csv file in ./sample_data

* To test another files
    1. Put files into ./sample_data
    2. Use the path of test file for input-file and spec-file.


## Assumption

* Each line of fixed width file always ends with newline character.
* The length of each line excluding last newline character should match with total of offests in spec.
* The output file is a csv file which has `,` delimiter and `"` escapechar.
* This tool does not strip any character in fields when a csv file is generated.
