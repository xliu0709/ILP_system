1. IP content
    - directory IPx
    - IPx.cpp
    - IPx.h
    - IPx_interface.csv ( specify top level function interface)
2. operation specification
    - named as IPx_ops.csv
    - first row: 
        op_id dependence  mem_offset  scalar_int scalar_float
    - op_id: the integer index for one operation on IPx, start from 0
    - dependence:  the op_id for the operations that current operation depends on. Seperated by comma, keep last comma. If no dependence, fill as None. example:
        1,2,4,

    - mem_offset: the starting byte address of the task. Same format as dependence
    - scalar_int: the integer scalar parameters. Same format as dependence
    - scalar_float: the float scalar parameters. Same format as dependence