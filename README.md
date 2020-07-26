# SavConv
Arbitrary console save file converter. 
Designed to help convert raw console save files to emulator supported saves.

Currently only supporing raw nds (.sav) to desmume (.dsv)

Dependencies:
Expects [python3](https://www.python.org/downloads/) to be installed and a command line interface to be available.

Usage:
```bash
python3 SavConv.py --help
python3 SavConv.py -i <raw-save.sav> -o <desmume-save.dsv>
python3 SavConv.py -i ~/POKEMON_D_ADAE01_05.sav -o ~/.config/desmume/POKEMON_D_ADAE01_05.trim.dsv
```

Note: the target save file probably needs to match the name of the rom you are using.

## Contribution details

More contribution information can be found in the python file(s).
Essentially try to stick to [PEP-8](https://www.python.org/dev/peps/pep-0008/), follow in-file styling at the very least, and make sure you dont break anything.
If this grows to support many different types of saves then we will need to set up better code infrastructure and put in CI/CD and/or unit tests.
