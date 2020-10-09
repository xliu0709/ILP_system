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


        

    print_list(script_command_list)
    # connecting HPM port

    # connecting HP port

    # connecting stream port

    # instanting BRAM

    # connecting 


            


        
                
        
        






