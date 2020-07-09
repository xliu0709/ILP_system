# Hardware Configuration Format
This file specifies how the ILP should specify the hardware 

# Required Information
## BRAM infomation dictionary
You need to provide a list of BRAM information with each item in the list including:
- **bram_name**: the name of the required BRAM buffer, example: BRAM_0
- **bram_width**: the bitwidth of the BRAM buffer,  example: 32
- **bram_depth**: the depth of the BRAM buffer: example: 1024
- **bram_addr_offset**: the address offset in AXI space in bytes, example:  32768

For perlimary design stability, the width should be 2^N, the depth should be 1024*N. We may try more flexible options after experiment.


## IP information dictionary
You need to provide a list of IP information with each item in the list including:
- **ip_name**: the name of the IP, example: "IP0"
- **hp_ports**: a list of string specifying which of the 4 HP port the IP is connected to, example: [HP0, HP1, HP2, HP3]

You can rename the current file by clicking the file name in the navigation bar or by clicking the **Rename** button in the file explorer.

# Format
The configuration file should be written in Yaml format.
## Example file
```
bram_info:
    BRAM_0:
        bram_name: BRAM_0
        bram_width: 32
        bram_depth: 1024
        bram_addr_offset: 0
    BRAM_1:
        bram_name: BRAM_1
        bram_width: 64
        bram_depth: 1024
        bram_addr_offset: 32768
ip_info:
    IP0:
        ip_name: IP0
        hp_ports: [HP0,HP1,HP2,HP3] 
```
## Format Detail

The example should be self-explanatory and can be viewed as the python dictionary structure. The indentation specifys the dictionary level. The string before the colon **:** is viewed as the key for current level of dictionary.  

**note**: the indentation should be constructed by spaces by the requirement of yaml. Perferably 4 spaces.
**note**: you don't need to add quote for the strings in the yaml file.

The configuration file should specify a dictionary with 2 keys: 
- string "bram_info": the key for bram information dictionary.  Each item in the dictionary should have its **bram_name** as its key.
- string "ip_info": the key for bram information dictionary.  Each item in the dictionary should have its **ip_name** as its key.

The file should be named as **block_config.yml**