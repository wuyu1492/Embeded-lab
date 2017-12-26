# Arduino File

### Prerequisites

HM-10

Import Arduino library: 
AltSoftSerial.h

### How to add customized characteristics
use AT mode

check AT mode
```
AT
```
if return OK, type:
```
AT+FFE2?
```
if return 1, type:
```
AT+RESET
```
