#ifndef _op_H_
#define _op_H_
#include <stdlib.h>
#include <vector>

class   op_info_t{
    public:
        int op_id;
        std::vector<int> dependence;
        std::vector<int> mem_offset_byte;
        std::vector<int> scalar_int;
        std::vector<float> scalar_float;
        op_info_t* next;
};

#endif




