#ifndef _PARSER_H_
#define _PARSER_H_

#include "op.h"
#include <fstream>
#include <sstream>
#include <string>
#include <iostream>
op_info_t* load_layer_info(
    char* filename);

#endif