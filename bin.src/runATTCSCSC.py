#!/usr/bin/env python

from lsst.ts.ATTCS import ATTCSCSC

csc = ATTCSCSC.ATTCSCsc(1)
csc.main(index=True)
