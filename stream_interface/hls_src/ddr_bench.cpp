#include <ap_int.h>
#include <hls_stream.h>
#include <ap_axi_sdata.h>

#define U_BITS 1
#define TI_BITS 1
#define TD_BITS 1

void stream_master(
	int length,
	int dest,
	int* DDR,
	hls::stream<ap_axis<32,U_BITS,TI_BITS,TD_BITS> > &out_stream
)
{
	#pragma HLS INTERFACE s_axilite register port=length
	#pragma HLS INTERFACE s_axilite register port=dest
	#pragma HLS interface m_axi port=DDR depth=65535 offset=slave bundle=HP1
	#pragma HLS INTERFACE axis port=out_stream
	#pragma HLS INTERFACE s_axilite register port=length
	#pragma HLS INTERFACE s_axilite register port=return

	ap_axis<32,U_BITS,TI_BITS,TD_BITS> data;
	for(int i=0;i<length;i++)
	{
		#pragma HLS pipeline
		data.data=DDR[i];
		data.dest=dest;
		data.id=0;
		data.user=0;
		out_stream<<data;
	}
}


void stream_slave(
	int length,
	int *DDR,
	hls::stream<ap_axis<32,U_BITS,TI_BITS,TD_BITS> > &in_stream
)
{
	#pragma HLS INTERFACE s_axilite register port=length
	#pragma HLS interface m_axi port=DDR depth=65535 offset=slave bundle=HP0
	#pragma HLS INTERFACE axis port=in_stream
	#pragma HLS INTERFACE s_axilite register port=return
	ap_axis<32,U_BITS,TI_BITS,TD_BITS> data;
	for(int i=0;i<length;i++)
	{
		#pragma HLS pipeline
		in_stream>>data;
		DDR[i]=data.data;
	}

}
