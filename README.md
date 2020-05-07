# DDOS MITIGATION SCRIPT

## SUPPORTED COMMANDS ARE

```
********************************************************************************
Supported Task: [DIVERT , NO_DIVERT, DIVERT_ALL, NO_DIVERT_ALL] 
********************************************************************************
DDOS MITIGATION TASK            :       no_divert
NETWORK ADDRESS                 :       113.61.58.0/24
```

### DIVERT
Divert a network to incapsula
```
==========  =================  ==========  ========
HOSTNAME    NETWORK ADDRESS    ACTIVITY    STATUS
==========  =================  ==========  ========
CORE-R1     113.61.58.0/24     DIVERT      FAILED
CORE-R2     113.61.58.0/24     DIVERT      FAILED
==========  =================  ==========  ========
```
### NO DIVERT
Remove the network to incapsula
```
==========  =================  ==========  ========
HOSTNAME    NETWORK ADDRESS    ACTIVITY    STATUS
==========  =================  ==========  ========
CORE-R1     113.61.58.0/24     NO_DIVERT   SUCCESS
CORE-R2     113.61.58.0/24     NO_DIVERT   FAILED
==========  =================  ==========  ========
```
### DIVERT ALL
Add all prefix to incapsula
```
==========  =================  ==========  ========
  HOSTNAME    NETWORK ADDRESS    ACTIVITY    STATUS
==========  =================  ==========  ========
CORE-R1     113.61.42 - 58.0   DIVERT_ALL  FAILED
CORE-R2     113.61.42 - 58.0   DIVERT_ALL  FAILED
==========  =================  ==========  ========
```

### NO DIVERT ALL
Removes all prefixes advertised in incapsula
```
==========  =================  =============  ========
  HOSTNAME    NETWORK ADDRESS       ACTIVITY    STATUS
==========  =================  =============  ========
CORE-R1     113.61.42 - 58.0   NO_DIVERT_ALL  FAILED
CORE-R2     113.61.42 - 58.0   NO_DIVERT_ALL  FAILED
==========  =================  =============  ========
```
