# create_project RTL ./RTL -part xczu9eg-ffvb1156-2-e
create_project RTL ./RTL -part xczu3eg-sbva484-1-e
# set_property board_part xilinx.com:zcu102:part0:3.3 [current_project]
set_property board_part em.avnet.com:ultra96v2:part0:1.0 [current_project]
create_bd_design "design_1"

create_bd_cell -type ip -vlnv xilinx.com:ip:zynq_ultra_ps_e:3.3 zynq_ultra_ps_e_0

apply_bd_automation -rule xilinx.com:bd_rule:zynq_ultra_ps_e -config {apply_board_preset "1" }  [get_bd_cells zynq_ultra_ps_e_0]
set_property -dict [list CONFIG.PSU__USE__M_AXI_GP1 {0} CONFIG.PSU__USE__S_AXI_GP1 {0} CONFIG.PSU__USE__S_AXI_GP2 {1} CONFIG.PSU__USE__S_AXI_GP3 {0} CONFIG.PSU__USE__S_AXI_GP4 {0} CONFIG.PSU__USE__S_AXI_GP5 {0} CONFIG.PSU__CRL_APB__PL0_REF_CTRL__FREQMHZ {250}] [get_bd_cells zynq_ultra_ps_e_0]
set_property -dict [list CONFIG.PSU__USE__IRQ0 {0}] [get_bd_cells zynq_ultra_ps_e_0]


set_property  ip_repo_paths  ./HLS [current_project]
update_ip_catalog
set IP_type stream_master
set IP_name stream_master_0

create_bd_cell -type ip -vlnv xilinx.com:hls:$IP_type:1.0 $IP_name

set IP_type stream_master
set IP_name stream_master_1
create_bd_cell -type ip -vlnv xilinx.com:hls:$IP_type:1.0 $IP_name


set IP_type stream_slave
set IP_name stream_slave_0
create_bd_cell -type ip -vlnv xilinx.com:hls:$IP_type:1.0 $IP_name


set IP_type stream_slave
set IP_name stream_slave_1
create_bd_cell -type ip -vlnv xilinx.com:hls:$IP_type:1.0 $IP_name


apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/zynq_ultra_ps_e_0/M_AXI_HPM0_FPD} Slave {/stream_master_0/s_axi_AXILiteS} intc_ip {New AXI Interconnect} master_apm {0}}  [get_bd_intf_pins stream_master_0/s_axi_AXILiteS]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)} Clk_slave {Auto} Clk_xbar {/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)} Master {/zynq_ultra_ps_e_0/M_AXI_HPM0_FPD} Slave {/stream_slave_0/s_axi_AXILiteS} intc_ip {/ps8_0_axi_periph} master_apm {0}}  [get_bd_intf_pins stream_slave_0/s_axi_AXILiteS]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)} Clk_slave {Auto} Clk_xbar {/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)} Master {/zynq_ultra_ps_e_0/M_AXI_HPM0_FPD} Slave {/stream_slave_1/s_axi_AXILiteS} intc_ip {/ps8_0_axi_periph} master_apm {0}}  [get_bd_intf_pins stream_slave_1/s_axi_AXILiteS]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)} Clk_slave {Auto} Clk_xbar {/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)} Master {/zynq_ultra_ps_e_0/M_AXI_HPM0_FPD} Slave {/stream_master_1/s_axi_AXILiteS} intc_ip {/ps8_0_axi_periph} master_apm {0}}  [get_bd_intf_pins stream_master_1/s_axi_AXILiteS]




apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/stream_slave_0/m_axi_HP0} Slave {/zynq_ultra_ps_e_0/S_AXI_HP0_FPD} intc_ip {Auto} master_apm {0}}  [get_bd_intf_pins zynq_ultra_ps_e_0/S_AXI_HP0_FPD]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)} Clk_xbar {/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)} Master {/stream_slave_1/m_axi_HP0} Slave {/zynq_ultra_ps_e_0/S_AXI_HP0_FPD} intc_ip {/axi_smc} master_apm {0}}  [get_bd_intf_pins stream_slave_1/m_axi_HP0]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)} Clk_slave {/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)} Clk_xbar {/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)} Master {/stream_master_1/m_axi_HP1} Slave {/zynq_ultra_ps_e_0/S_AXI_HP0_FPD} intc_ip {/axi_smc} master_apm {0}}  [get_bd_intf_pins stream_master_1/m_axi_HP1]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)} Clk_slave {/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)} Clk_xbar {/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)} Master {/stream_master_0/m_axi_HP1} Slave {/zynq_ultra_ps_e_0/S_AXI_HP0_FPD} intc_ip {/axi_smc} master_apm {0}}  [get_bd_intf_pins stream_master_0/m_axi_HP1]





create_bd_cell -type ip -vlnv xilinx.com:ip:axis_interconnect:2.1 axis_interconnect_0

set_property -dict [list CONFIG.NUM_SI {2}] [get_bd_cells axis_interconnect_0]
apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk "/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)" }  [get_bd_pins axis_interconnect_0/ACLK]


connect_bd_intf_net [get_bd_intf_pins stream_master_0/out_stream] -boundary_type upper [get_bd_intf_pins axis_interconnect_0/S00_AXIS]
apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk "/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)" }  [get_bd_pins axis_interconnect_0/S00_AXIS_ACLK]

connect_bd_intf_net [get_bd_intf_pins stream_master_1/out_stream] -boundary_type upper [get_bd_intf_pins axis_interconnect_0/S01_AXIS]
apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk "/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)" }  [get_bd_pins axis_interconnect_0/S01_AXIS_ACLK]

connect_bd_intf_net -boundary_type upper [get_bd_intf_pins axis_interconnect_0/M00_AXIS] [get_bd_intf_pins stream_slave_0/in_stream]
apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk "/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)" }  [get_bd_pins axis_interconnect_0/M00_AXIS_ACLK]
connect_bd_intf_net -boundary_type upper [get_bd_intf_pins axis_interconnect_0/M01_AXIS] [get_bd_intf_pins stream_slave_1/in_stream]
apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk "/zynq_ultra_ps_e_0/pl_clk0 (249 MHz)" }  [get_bd_pins axis_interconnect_0/M01_AXIS_ACLK]



make_wrapper -files [get_files ./RTL/RTL.srcs/sources_1/bd/design_1/design_1.bd] -top
add_files -norecurse ./RTL/RTL.srcs/sources_1/bd/design_1/hdl/design_1_wrapper.v

launch_runs impl_1 -to_step write_bitstream -jobs 16
wait_on_run impl_1
