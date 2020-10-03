############################################################
## This file is generated automatically by Vivado HLS.
## Please DO NOT edit it.
## Copyright (C) 1986-2019 Xilinx, Inc. All Rights Reserved.
############################################################
open_project HLS
set_top stream_master
add_files hls_src/ddr_bench.cpp
open_solution "solution1"
# set_part {xczu9eg-ffvb1156-2-e} -tool vivado
set_part {xczu3eg-sbva484-1-e} -tool vivado
create_clock -period 2 -name default
config_schedule -relax_ii_for_timing=0
#source "./HLS/solution1/directives.tcl"
#csim_design
csynth_design
#cosim_design
export_design -rtl verilog -format ip_catalog
