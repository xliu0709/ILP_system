import yaml
import sys

device_dict={
    "ultra96":{
        "fpga_part":"xczu3eg-sbva484-1-e",
        "board_part": "em.avnet.com:ultra96v2:part0:1.0"
    },
    "zcu102":{
        "fpga_part":"xczu9eg-ffvb1156-2-e",
        "board_part": "xilinx.com:zcu102:part0:3.3"
    }
}

frequency_divisor={
    100: (15,1),
    125: (12,1),
    150: (10,1),
    250: (6,1)
}




def load_op_yaml(filename):
    op_list_yaml=open(filename,"r")
    op_list=yaml.load(op_list_yaml)
    return op_list

def print_list(printlist):
    for i in printlist:
        print(i,end="")

if __name__ == "__main__":
    
    # load file name
    filename=sys.argv[1]
    hw_dict=load_op_yaml(filename)

    HW_configs=hw_dict["HW_configs"]
    IP_dict=hw_dict["IP_configs"]
    BRAM_dict=hw_dict["BRAM_configs"]


    IP_list=[]
    HP_port_list=[[],[],[],[]]
    BRAM_port_list=[]
    instream_port_list={}
    outstream_port_list=[]


    for key in IP_dict:
        if IP_dict[key]["IP_type"]=="BRAM":
            continue
        else:
            for i in range(4):
                if(IP_dict[key]["DDR_port"][i]!="None"):
                    HP_port_list[i].append( (key,IP_dict[key]["DDR_port"][i]))
            for bram_port_name in IP_dict[key]["BRAM_port"]:
                BRAM_port_list.append( (key,bram_port_name))
            for idx,instream_id in enumerate(IP_dict[key]["instream_port_id"]):
                instream_port_id=int(IP_dict[key]["instream_port_id"][idx])
                instream_port_name=IP_dict[key]["instream_port"][idx]
                assert(instream_id not in  instream_port_list)
                instream_port_list[instream_port_id]=(key,instream_port_name)
            for outstream_port_name in IP_dict[key]["outstream_port"]:
                outstream_port_list.append( (key,outstream_port_name) )
            IP_list.append( (key,IP_dict[key]["IP_type"]) )

    script_command_list=[]
    # create project
    script_str="\n# Creating Project\n"
    script_command_list.append(script_str)

    script_str="create_project RTL ./RTL -part "+HW_configs["fpga_name"]+"\n"
    script_command_list.append(script_str)

    
    script_str="set_property board_part "+ HW_configs["board_name"]+" [current_project]\n"
    script_command_list.append(script_str)

    

    # Creating block diagram
    script_str="\n# Creating block diagram\n"
    script_command_list.append(script_str)
    script_str="create_bd_design \"design_1\"\n"
    script_command_list.append(script_str)


    # Adding and configure MPSOC IP
    script_str="\n# Adding and configure MPSOC IP\n"
    script_command_list.append(script_str)

    script_str="create_bd_cell -type ip -vlnv xilinx.com:ip:zynq_ultra_ps_e:3.3 zynq_ultra_ps_e_0\n"
    script_command_list.append(script_str)

    script_str="apply_bd_automation -rule xilinx.com:bd_rule:zynq_ultra_ps_e -config {apply_board_preset \"1\" }  [get_bd_cells zynq_ultra_ps_e_0]\n"
    script_command_list.append(script_str)


    div0,div1=frequency_divisor[int(HW_configs["frequency"])]

    script_str="set_property -dict [list CONFIG.PSU__CRL_APB__PL0_REF_CTRL__DIVISOR0 {"+str(div0)+"} CONFIG.PSU__CRL_APB__PL0_REF_CTRL__DIVISOR1 {"+str(div1)+"}] [get_bd_cells zynq_ultra_ps_e_0]\n"
    script_command_list.append(script_str)
    

    script_str="set_property -dict [list CONFIG.PSU__USE__M_AXI_GP1 {1}] [get_bd_cells zynq_ultra_ps_e_0]\n"
    script_command_list.append(script_str)
    script_str="set_property -dict [list CONFIG.PSU__USE__M_AXI_GP1 {0}] [get_bd_cells zynq_ultra_ps_e_0]\n"
    script_command_list.append(script_str)

    if(len(HP_port_list[0])!=0):
        script_str="set_property -dict [list CONFIG.PSU__USE__S_AXI_GP2 {1}] [get_bd_cells zynq_ultra_ps_e_0]\n"
        script_command_list.append(script_str)
    else:
        script_str="set_property -dict [list CONFIG.PSU__USE__S_AXI_GP2 {0}] [get_bd_cells zynq_ultra_ps_e_0]\n"
        script_command_list.append(script_str)
    if(len(HP_port_list[1])!=0):
        script_str="set_property -dict [list CONFIG.PSU__USE__S_AXI_GP3 {1}] [get_bd_cells zynq_ultra_ps_e_0]\n"
        script_command_list.append(script_str)
    else:
        script_str="set_property -dict [list CONFIG.PSU__USE__S_AXI_GP3 {0}] [get_bd_cells zynq_ultra_ps_e_0]\n"
        script_command_list.append(script_str)
    if(len(HP_port_list[2])!=0):
        script_str="set_property -dict [list CONFIG.PSU__USE__S_AXI_GP4 {1}] [get_bd_cells zynq_ultra_ps_e_0]\n"
        script_command_list.append(script_str)
    else:
        script_str="set_property -dict [list CONFIG.PSU__USE__S_AXI_GP4 {0}] [get_bd_cells zynq_ultra_ps_e_0]\n"
        script_command_list.append(script_str)
    if(len(HP_port_list[3])!=0):
        script_str="set_property -dict [list CONFIG.PSU__USE__S_AXI_GP5 {1}] [get_bd_cells zynq_ultra_ps_e_0]\n"
        script_command_list.append(script_str)
    else:
        script_str="set_property -dict [list CONFIG.PSU__USE__S_AXI_GP5 {0}] [get_bd_cells zynq_ultra_ps_e_0]\n"
        script_command_list.append(script_str)

   

    # Adding IPs
    script_str="\n# Adding IPs\n"
    script_command_list.append(script_str)


    script_str="set_property  ip_repo_paths  "+HW_configs["IP_repo_path"]+" [current_project]\n"
    script_command_list.append(script_str)
    script_str="update_ip_catalog\n"
    script_command_list.append(script_str)


    for item in IP_list:
        IP_name,IP_type = item
        script_str="create_bd_cell -type ip -vlnv xilinx.com:hls:"+IP_type+":1.0 "+IP_name+"\n"
        script_command_list.append(script_str)


        

    # connecting HPM port
    script_str="\n# Connecting HPM port\n"
    script_command_list.append(script_str)

    first=True
    for item in IP_list:
        IP_name,IP_type = item
        if(first):
            script_str="apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/zynq_ultra_ps_e_0/M_AXI_HPM0_FPD} Slave {/"+IP_name+"/s_axi_AXILiteS} intc_ip {New AXI Interconnect} master_apm {0}}  [get_bd_intf_pins "+IP_name+"/s_axi_AXILiteS]\n"
        else:
            script_str="apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {/zynq_ultra_ps_e_0/pl_clk0} Clk_slave {Auto} Clk_xbar {/zynq_ultra_ps_e_0/pl_clk0} Master {/zynq_ultra_ps_e_0/M_AXI_HPM0_FPD} Slave {/"+IP_name+"/s_axi_AXILiteS} intc_ip {/ps8_0_axi_periph} master_apm {0}}  [get_bd_intf_pins "+IP_name+"/s_axi_AXILiteS]\n"
        first=False
        script_command_list.append(script_str)        


   
    # Connecting HP port
    script_str="\n# Connecting HP port\n"
    script_command_list.append(script_str)

    for HP_port_idx,port_mapping_list in enumerate(HP_port_list):
        first=True
        script_command_list.append("\n")
        for item in port_mapping_list:
            IP_name,port_name = item
            if(first):
                script_str="apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {Auto} Clk_xbar {Auto} Master {/"+IP_name+"/m_axi_"+port_name+"} Slave {/zynq_ultra_ps_e_0/S_AXI_HP+"+str(HP_port_idx)+"_FPD} intc_ip {Auto} master_apm {0}}  [get_bd_intf_pins zynq_ultra_ps_e_0/S_AXI_HP"+str(HP_port_idx)+"_FPD]\n"
            else:
                script_str="apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {Auto} Clk_slave {/zynq_ultra_ps_e_0/pl_clk0} Clk_xbar {/zynq_ultra_ps_e_0/pl_clk0} Master {/"+IP_name+"/m_axi_"+port_name+"} Slave {/zynq_ultra_ps_e_0/S_AXI_HP"+str(HP_port_idx)+"_FPD} intc_ip {/axi_smc} master_apm {0}}  [get_bd_intf_pins "+IP_name+"/m_axi_"+port_name+"]\n"


            first=False
            script_command_list.append(script_str)
  
    # Connecting stream port

    script_str="\n# Connecting stream port\n"
    script_command_list.append(script_str)
    script_str="create_bd_cell -type ip -vlnv xilinx.com:ip:axis_interconnect:2.1 axis_interconnect_0\n"
    script_command_list.append(script_str)
    

    
    script_str="set_property -dict [list CONFIG.NUM_SI {"+str(len(outstream_port_list))+"}] [get_bd_cells axis_interconnect_0]\n"
    script_command_list.append(script_str)

    script_str="set_property -dict [list CONFIG.NUM_MI {"+str(len(instream_port_list))+"}] [get_bd_cells axis_interconnect_0]\n"
    script_command_list.append(script_str)

    script_str="apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk \"/zynq_ultra_ps_e_0/pl_clk0\" }  [get_bd_pins axis_interconnect_0/ACLK]\n"
    script_command_list.append(script_str)   

    for outstream_port_idx,item in enumerate(outstream_port_list):
        IP_name,stream_port_name=item
 
        script_str="connect_bd_intf_net [get_bd_intf_pins "+IP_name+"/"+stream_port_name+"] -boundary_type upper [get_bd_intf_pins axis_interconnect_0/S"+'{0:02}'.format(outstream_port_idx)+"_AXIS]\n"
        script_command_list.append(script_str)
        script_str="apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk \"/zynq_ultra_ps_e_0/pl_clk0\" }  [get_bd_pins axis_interconnect_0/S"+'{0:02}'.format(outstream_port_idx)+"_AXIS_ACLK]\n"
        script_command_list.append(script_str)

    script_command_list.append("\n")
    for key,item in instream_port_list.items():
        IP_name,stream_port_name=item
        script_str="connect_bd_intf_net -boundary_type upper [get_bd_intf_pins axis_interconnect_0/M"+'{0:02}'.format(key)+"_AXIS] [get_bd_intf_pins "+IP_name+"/"+stream_port_name+"]\n"
        script_command_list.append(script_str)
        script_str="apply_bd_automation -rule xilinx.com:bd_rule:clkrst -config {Clk \"/zynq_ultra_ps_e_0/pl_clk0\" }  [get_bd_pins axis_interconnect_0/M"+'{0:02}'.format(key)+"_AXIS_ACLK]\n"
        script_command_list.append(script_str)





    # Instanting BRAM
    script_str="\n# Instanting BRAM\n"
    script_command_list.append(script_str)

    for key,BRAM_info in BRAM_dict.items():
        script_command_list.append("\n")
        width=int(BRAM_info["width"])
        depth=int(BRAM_info["depth"])
        script_str="create_bd_cell -type ip -vlnv xilinx.com:ip:blk_mem_gen:8.4 "+key+"\n"
        script_command_list.append(script_str)
        script_str="set_property -dict [list CONFIG.Enable_32bit_Address {false} CONFIG.Use_Byte_Write_Enable {false} CONFIG.Byte_Size {9} CONFIG.Register_PortA_Output_of_Memory_Primitives {true} CONFIG.Use_RSTA_Pin {false} CONFIG.use_bram_block {Stand_Alone} CONFIG.EN_SAFETY_CKT {false}] [get_bd_cells "+key+"]\n"
        script_command_list.append(script_str)
        script_str="set_property -dict [list CONFIG.Write_Width_A {} CONFIG.Write_Depth_A {} CONFIG.Read_Width_A {}] [get_bd_cells {}]\n".format(width,depth,width,key)
        script_command_list.append(script_str)
        script_str="set_property -dict [list CONFIG.Write_Width_B {} CONFIG.Read_Width_B {}] [get_bd_cells {}]\n".format(width,width,key)
        script_command_list.append(script_str)
        script_str="create_bd_cell -type ip -vlnv xilinx.com:ip:axi_bram_ctrl:4.1 axi_bram_ctrl_"+key+"\n"
        script_command_list.append(script_str)
        script_str="apply_bd_automation -rule xilinx.com:bd_rule:bram_cntlr -config {BRAM \"/"+key+"\" }  [get_bd_intf_pins axi_bram_ctrl_"+key+"/BRAM_PORTA]\n"
        script_command_list.append(script_str)
        script_str="apply_bd_automation -rule xilinx.com:bd_rule:bram_cntlr -config {BRAM \"/"+key+"\" }  [get_bd_intf_pins axi_bram_ctrl_"+key+"/BRAM_PORTB]\n"
        script_command_list.append(script_str)




    # Connecting BRAM
    script_str="\n# Connecting BRAM\n"
    script_command_list.append(script_str)

    if(len(BRAM_dict)!=0):
        IP_name,bram_port_name=BRAM_port_list[0]
        idx=0;

        for key in BRAM_dict:
            if(idx==0): 
                first_BRAM_name=key
                script_str="apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {/zynq_ultra_ps_e_0/pl_clk0} Clk_slave {Auto} Clk_xbar {Auto} Master {/"+IP_name+"/m_axi_"+bram_port_name+"} Slave {/axi_bram_ctrl_"+key+"/S_AXI} intc_ip {New AXI Interconnect} master_apm {0}}  [get_bd_intf_pins axi_bram_ctrl_"+key+"/S_AXI]\n"
                script_command_list.append(script_str)
            else:
                script_str="apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {/zynq_ultra_ps_e_0/pl_clk0} Clk_slave {Auto} Clk_xbar {/zynq_ultra_ps_e_0/pl_clk0} Master {/"+IP_name+"/m_axi_"+bram_port_name+"} Slave {/axi_bram_ctrl_"+key+"/S_AXI} intc_ip {/axi_mem_intercon} master_apm {0}}  [get_bd_intf_pins axi_bram_ctrl_"+key+"/S_AXI]"
                script_command_list.append(script_str)

       
                
    for idx,item in enumerate(BRAM_port_list):
        if idx==0:continue
        IP_name,bram_port_name=item

        script_str="apply_bd_automation -rule xilinx.com:bd_rule:axi4 -config { Clk_master {/zynq_ultra_ps_e_0/pl_clk0} Clk_slave {/zynq_ultra_ps_e_0/pl_clk0} Clk_xbar {/zynq_ultra_ps_e_0/pl_clk0} Master {/"+IP_name+"/m_axi_"+bram_port_name+"} Slave {/axi_bram_ctrl_"+first_BRAM_name+"/S_AXI} intc_ip {/axi_mem_intercon} master_apm {0}}  [get_bd_intf_pins "+IP_name+"/m_axi_"+bram_port_name+"]\n"
        script_command_list.append(script_str)

    print_list(script_command_list)  

    # Configuring BRAM address
    script_str="\n# Configuring BRAM address\n"
    script_command_list.append(script_str)


    for idx,item in enumerate(BRAM_port_list):
        IP_name,bram_port_name=item
        for bram_name in BRAM_dict:
            address_str="{:08x}".format(BRAM_dict[bram_name]["byte_address_offset"])
            script_str="set_property offset 0x"+address_str+" [get_bd_addr_segs {"+IP_name+"/Data_m_axi_"+bram_port_name+"/SEG_axi_bram_ctrl_"+bram_name+"_Mem0}]\n"
            script_command_list.append(script_str)
            script_str="set_property range "+BRAM_dict[bram_name]["range"]+" [get_bd_addr_segs {"+IP_name+"/Data_m_axi_"+bram_port_name+"/SEG_axi_bram_ctrl_"+bram_name+"_Mem0}]\n"
            script_command_list.append(script_str)        


    # Syn and impl
    script_str="\n# Syn and impl\n"
    script_command_list.append(script_str)

    script_str="make_wrapper -files [get_files ./RTL/RTL.srcs/sources_1/bd/design_1/design_1.bd] -top\n"
    script_command_list.append(script_str)
    script_str="add_files -norecurse ./RTL/RTL.srcs/sources_1/bd/design_1/hdl/design_1_wrapper.v\n"
    script_command_list.append(script_str)
    script_str="launch_runs impl_1 -to_step write_bitstream -jobs 16\n"
    script_command_list.append(script_str)
    script_str="wait_on_run impl_1\n"
    script_command_list.append(script_str)

    print_list(script_command_list)  

    script_file=open("auto_script.tcl","w")
    for i in script_command_list:
        script_file.write(i)
    script_file.close()




