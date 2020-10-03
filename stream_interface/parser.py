
import yaml
import numpy
import sys

import threading 
import time

from pynq import Xlnk
from pynq import Overlay





def load_op_yaml(filename):
    op_list_yaml=open(filename,"r")
    op_list=yaml.load(op_list_yaml)
    return op_list


def process_task(op_list,initial_ddr_addr):
    op_list_by_IP={}
    op_param_by_IP={}
    op_dep_by_IP={}
    op_id_by_IP={}
    for task in op_list:
        IP_name=task["IP_name"]
        if IP_name not in op_list_by_IP:
            op_list_by_IP[IP_name]=[]
            op_param_by_IP[IP_name]=[]
            op_dep_by_IP[IP_name]=[]
            op_id_by_IP[IP_name]=[]
        
        int_scalar_np=numpy.array(task["int_scalar"],dtype="int32")
        float_scalar_np=numpy.array(task["float_scalar"],dtype="float32").view(dtype="int32")
        BRAM_offset_np=numpy.array(task["BRAM_offsets"],dtype="int32")
        DDR_offset_np=numpy.array(task["DDR_offsets"],dtype="int32")
    
        for i in range(DDR_offset_np.size):
            DDR_offset_np[i]+=initial_ddr_addr


        all_parameter=numpy.concatenate((int_scalar_np,float_scalar_np,BRAM_offset_np,DDR_offset_np) ).tolist()
        
        op_list_by_IP[IP_name].append(task)
        op_param_by_IP[IP_name].append(all_parameter)
        op_dep_by_IP[IP_name].append(task["dependence"])
        op_id_by_IP[IP_name].append(task["op_id"])


    return op_list_by_IP,op_param_by_IP,op_dep_by_IP,op_id_by_IP



def exec_op_list(
    IP_name,
    op_dep_list,
    op_param_list,
    op_id_list,
    overlay
    ):

    
    print(IP_name,"start")
    global op_done_flag
    for i,param in enumerate(op_param_list):
        
        dep=op_dep_list[i]
        idx=op_id_list[i]
        dep_fufill=False
        print(IP_name,"Operation ", idx)
        print(param)
        while(not dep_fufill):
            dep_done=True
            #read lock
            for j in dep:
                dep_done=dep_done and op_done_flag[j]
            #read lock release
            # exec(task)
            dep_fufill=dep_done
        for i in range(len(param)):
            overlay.write(0x10+i*8,param[i])
        
        overlay.write(0x10,arg[1])
        overlay.write(0x18,arg[2])
        overlay.write(0x20,arg[3])    

        
        overlay.write(0x00, 1)
        isready = overlay.read(0x00)
        while( isready == 1 ):
            isready = overlay.read(0x00)
        
        print(IP_name,"Operation done", idx)
        #write_lock
        op_done_flag[idx]=True
        #write lock release

            






if __name__ == "__main__":
    
    # load overlay
    
    xlnk = Xlnk()
    xlnk.xlnk_reset()

    mem_blk = xlnk.cma_array(shape=(4096), dtype=numpy.int32)

    for i in range(256):
        mem_blk[i]=i

    # for i in range(128):
    #     mem_blk[128+i]=128-i

    overlay = Overlay("design_1_wrapper.bit")
    print("bitstream loaded")


    # for i in range(16384):
    #     mem_blk[i]=255;


    
    # load file name
    filename=sys.argv[1]
    op_list=load_op_yaml(filename)
    

    # load_op_done

    global op_done_flag
    op_length=len(op_list["task"])
    op_done_flag=[False]*op_length
    
    op_list_by_IP,op_param_by_IP,op_dep_by_IP,op_id_by_IP=process_task(op_list["task"],mem_blk.physical_address)

    
    threads=[]
    IPs=[]

    for k in op_list_by_IP:
        IP=getattr(overlay,k)
        # IP=0
        IPs.append(IP)
        t=threading.Thread(target=exec_op_list, args=(k,op_dep_by_IP[k],op_param_by_IP[k],op_id_by_IP[k],IP))
        threads.append(t)

    
    for i in threads:
        i.start()
    
    for i in threads:
        i.join()

    for i in range(256):
        print(mem_blk[256+i])
    
        

    



    
    


        
        



