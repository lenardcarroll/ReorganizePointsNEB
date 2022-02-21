# ReorganizePointsNEB

This script eorganizes non-fixed coordinates from the input and output file for an NEB Band calculation as to allow for the least movement of atoms. The script's general command works like this:

```
python -i ReorganizePoint.py -inp <INPUT_FILE_NAME> -out <OUTPUT_FILE_NAME>
```

Make sure the input file contains only non-frozen atoms, that is, if input file had frozen atoms, remove them first.

The script works by taking the final coordinates and then calculating the midpoint of it. The initial coordinates are then used and the distance calculated between it and the midpoint. The atom that has the longest distance is placed first in the list, and the shortest last.

Next, the distance between the sorted initial coordinates and the final coordinates are calculated, with shortest distance aimed for.
