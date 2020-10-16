
# Creating Project
create_project RTL ./RTL -part xczu3eg-sbva484-1-e
set_property board_part em.avnet.com:ultra96v2:part0:1.0 [current_project]

# Creating block diagram
create_bd_design "design_1"

# Adding and configure MPSOC IP
create_bd_cell -type ip -vlnv xilinx.com:ip:zynq_ultra_ps_e:3.3 zynq_ultra_ps_e_0
apply_bd_automation -rule xilinx.com:bd_rule:zynq_ultra_ps_e -config {apply_board_preset "1" }  [get_bd_cells zynq_ultra_ps_e_0]
set_property -dict [list CONFIG.PSU__CRL_APB__PL0_REF_CTRL__DIVISOR0 {6} CONFIG.PSU__CRL_APB__PL0_REF_CTRL__DIVISOR1 {1}] [get_bd_cells zynq_ultra_ps_e_0]
set_property -dict [list CONFIG.PSU__USE__M_AXI_GP1 {1}] [get_bd_cells zynq_ultra_ps_e_0]
set_property -dict [list CONFIG.PSU__USE__M_AXI_GP1 {0}] [get_bd_cells zynq_ultra_ps_e_0]
set_property -dict [list CONFIG.PSU__USE__S_AXI_GP2 {1}] [get_bd_cells zynq_ultra_ps_e_0]
set_property -dict [list CONFIG.PSU__USE__S_AXI_GP3 {1}] [get_bd_cells zynq_ultra_ps_e_0]
set_property -dict [list CONFIG.PSU__USE__S_AXI_GP4 {0}] [get_bd_cells zynq_ultra_ps_e_0]
set_property -dict [list CONFIG.PSU__USE__S_AXI_GP5 {0}] [get_bd_cells zynq_ultra_ps_e_0]

# Adding IPs
set_property  ip_repo_paths  ./HLS [current_project]
update_ip_catalog
create_bd_cell -type ip -vlnv xilinx.com:hls:testing_IP0:1.0 IP0
create_bd_cell -type ip -vlnv xilinx.com:hls:testing_IP1:1.0 IP1

# Connecting HPM port
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/zynq_ultra_ps_e_0/M_AXI_HPM0_FPD} Slave {/IP0/s_axi_AXILiteS} intc_ip {New AXI Interconnect} master_apm {0}}  [get_bd_intf_pins IP0/s_axi_AXILiteS]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {/zynq_ultra_ps_e_0/pl_clk0} Clk_slave {Auto} Clk_xbar {/zynq_ultra_ps_e_0/pl_clk0} Master {/zynq_ultra_ps_e_0/M_AXI_HPM0_FPD} Slave {/IP1/s_axi_AXILiteS} intc_ip {/ps8_0_axi_periph} master_apm {0}}  [get_bd_intf_pins IP1/s_axi_AXILiteS]

# Connecting HP port

apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/IP0/m_axi_HP0} Slave {/zynq_ultra_ps_e_0/S_AXI_HP+0_FPD} intc_ip {Auto} master_apm {0}}  [get_bd_intf_pins zynq_ultra_ps_e_0/S_AXI_HP0_FPD]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {/zynq_ultra_ps_e_0/pl_clk0} Clk_xbar {/zynq_ultra_ps_e_0/pl_clk0} Master {/IP1/m_axi_HP0} Slave {/zynq_ultra_ps_e_0/S_AXI_HP0_FPD} intc_ip {/axi_smc} master_apm {0}}  [get_bd_intf_pins IP1/m_axi_HP0]

apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/IP0/m_axi_HP1} Slave {/zynq_ultra_ps_e_0/S_AXI_HP+1_FPD} intc_ip {Auto} master_apm {0}}  [get_bd_intf_pins zynq_ultra_ps_e_0/S_AXI_HP1_FPD]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {/zynq_ultra_ps_e_0/pl_clk0} Clk_xbar {/zynq_ultra_ps_e_0/pl_clk0} Master {/IP1/m_axi_HP1} Slave {/zynq_ultra_ps_e_0/S_AXI_HP1_FPD} intc_ip {/axi_smc} master_apm {0}}  [get_bd_intf_pins IP1/m_axi_HP1]



# Connecting stream port
create_bd_cell -type ip -vlnv xilinx.com:ip:axis_interconnect:2.1 axis_interconnect_0
set_property -dict [list CONFIG.NUM_SI {2}] [get_bd_cells axis_interconnect_0]
set_property -dict [list CONFIG.NUM_MI {2}] [get_bd_cells axis_interconnect_0]
apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk "/zynq_ultra_ps_e_0/pl_clk0" }  [get_bd_pins axis_interconnect_0/ACLK]
connect_bd_intf_net [get_bd_intf_pins IP0/OSTREAM] -boundary_type upper [get_bd_intf_pins axis_interconnect_0/S00_AXIS]
apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk "/zynq_ultra_ps_e_0/pl_clk0" }  [get_bd_pins axis_interconnect_0/S00_AXIS_ACLK]
connect_bd_intf_net [get_bd_intf_pins IP1/OSTREAM] -boundary_type upper [get_bd_intf_pins axis_interconnect_0/S01_AXIS]
apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk "/zynq_ultra_ps_e_0/pl_clk0" }  [get_bd_pins axis_interconnect_0/S01_AXIS_ACLK]

connect_bd_intf_net -boundary_type upper [get_bd_intf_pins axis_interconnect_0/M00_AXIS] [get_bd_intf_pins IP0/ISTREAM]
apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk "/zynq_ultra_ps_e_0/pl_clk0" }  [get_bd_pins axis_interconnect_0/M00_AXIS_ACLK]
connect_bd_intf_net -boundary_type upper [get_bd_intf_pins axis_interconnect_0/M01_AXIS] [get_bd_intf_pins IP1/ISTREAM]
apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk "/zynq_ultra_ps_e_0/pl_clk0" }  [get_bd_pins axis_interconnect_0/M01_AXIS_ACLK]

# Instanting BRAM

create_bd_cell -type ip -vlnv xilinx.com:ip:blk_mem_gen:8.4 BRAM0
set_property -dict [list CONFIG.Enable_32bit_Address {false} CONFIG.Use_Byte_Write_Enable {false} CONFIG.Byte_Size {9} CONFIG.Register_PortA_Output_of_Memory_Primitives {true} CONFIG.Use_RSTA_Pin {false} CONFIG.use_bram_block {Stand_Alone} CONFIG.EN_SAFETY_CKT {false}] [get_bd_cells BRAM0]
set_property -dict [list CONFIG.Write_Width_A 128 CONFIG.Write_Depth_A 1024 CONFIG.Read_Width_A 128] [get_bd_cells BRAM0]
set_property -dict [list CONFIG.Write_Width_B 128 CONFIG.Read_Width_B 128] [get_bd_cells BRAM0]
create_bd_cell -type ip -vlnv xilinx.com:ip:axi_bram_ctrl:4.1 axi_bram_ctrl_BRAM0
apply_bd_automation -rule xilinx.com:bd_rule:bram_cntlr -config {BRAM "/BRAM0" }  [get_bd_intf_pins axi_bram_ctrl_BRAM0/BRAM_PORTA]
apply_bd_automation -rule xilinx.com:bd_rule:bram_cntlr -config {BRAM "/BRAM0" }  [get_bd_intf_pins axi_bram_ctrl_BRAM0/BRAM_PORTB]

create_bd_cell -type ip -vlnv xilinx.com:ip:blk_mem_gen:8.4 BRAM1
set_property -dict [list CONFIG.Enable_32bit_Address {false} CONFIG.Use_Byte_Write_Enable {false} CONFIG.Byte_Size {9} CONFIG.Register_PortA_Output_of_Memory_Primitives {true} CONFIG.Use_RSTA_Pin {false} CONFIG.use_bram_block {Stand_Alone} CONFIG.EN_SAFETY_CKT {false}] [get_bd_cells BRAM1]
set_property -dict [list CONFIG.Write_Width_A 128 CONFIG.Write_Depth_A 1024 CONFIG.Read_Width_A 128] [get_bd_cells BRAM1]
set_property -dict [list CONFIG.Write_Width_B 128 CONFIG.Read_Width_B 128] [get_bd_cells BRAM1]
create_bd_cell -type ip -vlnv xilinx.com:ip:axi_bram_ctrl:4.1 axi_bram_ctrl_BRAM1
apply_bd_automation -rule xilinx.com:bd_rule:bram_cntlr -config {BRAM "/BRAM1" }  [get_bd_intf_pins axi_bram_ctrl_BRAM1/BRAM_PORTA]
apply_bd_automation -rule xilinx.com:bd_rule:bram_cntlr -config {BRAM "/BRAM1" }  [get_bd_intf_pins axi_bram_ctrl_BRAM1/BRAM_PORTB]

# Connecting BRAM
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {/zynq_ultra_ps_e_0/pl_clk0} Clk_slave {Auto} Clk_xbar {Auto} Master {/IP0/m_axi_BRAM0} Slave {/axi_bram_ctrl_BRAM0/S_AXI} intc_ip {New AXI Interconnect} master_apm {0}}  [get_bd_intf_pins axi_bram_ctrl_BRAM0/S_AXI]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {/zynq_ultra_ps_e_0/pl_clk0} Clk_slave {Auto} Clk_xbar {Auto} Master {/IP0/m_axi_BRAM0} Slave {/axi_bram_ctrl_BRAM1/S_AXI} intc_ip {New AXI Interconnect} master_apm {0}}  [get_bd_intf_pins axi_bram_ctrl_BRAM1/S_AXI]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {/zynq_ultra_ps_e_0/pl_clk0} Clk_slave {/zynq_ultra_ps_e_0/pl_clk0} Clk_xbar {/zynq_ultra_ps_e_0/pl_clk0} Master {/IP0/m_axi_BRAM1} Slave {/axi_bram_ctrl_BRAM1/S_AXI} intc_ip {/axi_mem_intercon} master_apm {0}}  [get_bd_intf_pins IP0/m_axi_BRAM1]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {/zynq_ultra_ps_e_0/pl_clk0} Clk_slave {/zynq_ultra_ps_e_0/pl_clk0} Clk_xbar {/zynq_ultra_ps_e_0/pl_clk0} Master {/IP1/m_axi_BRAM0} Slave {/axi_bram_ctrl_BRAM1/S_AXI} intc_ip {/axi_mem_intercon} master_apm {0}}  [get_bd_intf_pins IP1/m_axi_BRAM0]
apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {/zynq_ultra_ps_e_0/pl_clk0} Clk_slave {/zynq_ultra_ps_e_0/pl_clk0} Clk_xbar {/zynq_ultra_ps_e_0/pl_clk0} Master {/IP1/m_axi_BRAM1} Slave {/axi_bram_ctrl_BRAM1/S_AXI} intc_ip {/axi_mem_intercon} master_apm {0}}  [get_bd_intf_pins IP1/m_axi_BRAM1]

# Configuring BRAM address
set_property offset 0x00000000 [get_bd_addr_segs {IP0/Data_m_axi_BRAM0/SEG_axi_bram_ctrl_BRAM0_Mem0}]
set_property range 16K [get_bd_addr_segs {IP0/Data_m_axi_BRAM0/SEG_axi_bram_ctrl_BRAM0_Mem0}]
set_property offset 0x00004000 [get_bd_addr_segs {IP0/Data_m_axi_BRAM0/SEG_axi_bram_ctrl_BRAM1_Mem0}]
set_property range 16K [get_bd_addr_segs {IP0/Data_m_axi_BRAM0/SEG_axi_bram_ctrl_BRAM1_Mem0}]
set_property offset 0x00000000 [get_bd_addr_segs {IP0/Data_m_axi_BRAM1/SEG_axi_bram_ctrl_BRAM0_Mem0}]
set_property range 16K [get_bd_addr_segs {IP0/Data_m_axi_BRAM1/SEG_axi_bram_ctrl_BRAM0_Mem0}]
set_property offset 0x00004000 [get_bd_addr_segs {IP0/Data_m_axi_BRAM1/SEG_axi_bram_ctrl_BRAM1_Mem0}]
set_property range 16K [get_bd_addr_segs {IP0/Data_m_axi_BRAM1/SEG_axi_bram_ctrl_BRAM1_Mem0}]
set_property offset 0x00000000 [get_bd_addr_segs {IP1/Data_m_axi_BRAM0/SEG_axi_bram_ctrl_BRAM0_Mem0}]
set_property range 16K [get_bd_addr_segs {IP1/Data_m_axi_BRAM0/SEG_axi_bram_ctrl_BRAM0_Mem0}]
set_property offset 0x00004000 [get_bd_addr_segs {IP1/Data_m_axi_BRAM0/SEG_axi_bram_ctrl_BRAM1_Mem0}]
set_property range 16K [get_bd_addr_segs {IP1/Data_m_axi_BRAM0/SEG_axi_bram_ctrl_BRAM1_Mem0}]
set_property offset 0x00000000 [get_bd_addr_segs {IP1/Data_m_axi_BRAM1/SEG_axi_bram_ctrl_BRAM0_Mem0}]
set_property range 16K [get_bd_addr_segs {IP1/Data_m_axi_BRAM1/SEG_axi_bram_ctrl_BRAM0_Mem0}]
set_property offset 0x00004000 [get_bd_addr_segs {IP1/Data_m_axi_BRAM1/SEG_axi_bram_ctrl_BRAM1_Mem0}]
set_property range 16K [get_bd_addr_segs {IP1/Data_m_axi_BRAM1/SEG_axi_bram_ctrl_BRAM1_Mem0}]

# Syn and impl
make_wrapper -files [get_files ./RTL/RTL.srcs/sources_1/bd/design_1/design_1.bd] -top
add_files -norecurse ./RTL/RTL.srcs/sources_1/bd/design_1/hdl/design_1_wrapper.v
launch_runs impl_1 -to_step write_bitstream -jobs 16
wait_on_run impl_1
