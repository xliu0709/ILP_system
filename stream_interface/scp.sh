BOARD_ADDRESS="192.168.3.1"
sshpass -p 'xilinx' scp  RTL/RTL.runs/impl_1/design_1_wrapper.bit xilinx@$BOARD_ADDRESS:design_1_wrapper.bit
sshpass -p 'xilinx' scp  RTL/RTL.srcs/sources_1/bd/design_1/hw_handoff/design_1.hwh  xilinx@$BOARD_ADDRESS:design_1_wrapper.hwh
sshpass -p 'xilinx' scp  hardware.py xilinx@$BOARD_ADDRESS:hardware.py
sshpass -p 'xilinx' scp  parser.py xilinx@$BOARD_ADDRESS:parser.py
sshpass -p 'xilinx' scp  op0.yml xilinx@$BOARD_ADDRESS:op0.yml