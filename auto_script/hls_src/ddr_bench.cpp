#include <ap_int.h>
#include <hls_stream.h>
#include <ap_axi_sdata.h>

#define U_BITS 1
#define TI_BITS 1
#define TD_BITS 1

void testing_IP0(
	int mode,
	int length,
	int dest,
	ap_uint<128>* BRAM0,
	ap_uint<128>* BRAM1,	
	ap_uint<128>* DDR0,
	ap_uint<128>* DDR1,
	hls::stream<ap_axis<128,U_BITS,TI_BITS,TD_BITS> > &ISTREAM,
	hls::stream<ap_axis<128,U_BITS,TI_BITS,TD_BITS> > &OSTREAM
)
{
	#pragma HLS INTERFACE s_axilite register port=mode
	#pragma HLS INTERFACE s_axilite register port=length
	#pragma HLS INTERFACE s_axilite register port=dest
	
	#pragma HLS interface m_axi port=DDR0 depth=65535 offset=slave bundle=HP0 name=HP0
	#pragma HLS interface m_axi port=DDR1 depth=65535 offset=slave bundle=HP1 name=HP1
	#pragma HLS interface m_axi port=BRAM0 depth=65535 offset=slave bundle=BRAM0 name=BRAM0
	#pragma HLS interface m_axi port=BRAM1 depth=65535 offset=slave bundle=BRAM1 name=BRAM1


	#pragma HLS INTERFACE axis port=ISTREAM name=ISTREAM
	#pragma HLS INTERFACE axis port=OSTREAM	name=OSTREAM
	#pragma HLS INTERFACE s_axilite register port=return

	ap_axis<128,U_BITS,TI_BITS,TD_BITS> data;

	if(mode==0) //DDR to BRAM
	{
		for(int i=0;i<length;i++)
		{
			#pragma HLS pipeline
			BRAM0[i]=DDR0[i];
			BRAM1[i]=DDR1[i];
		}
	}
	else if (mode==1) //BRAM to DDR
	{
		for(int i=0;i<length;i++)
		{
			#pragma HLS pipeline
			DDR0[i]=BRAM0[i];
			DDR1[i]=BRAM1[i];
		}
	}
	else if (mode==2) //BRAM to BRAM
	{
		for(int i=0;i<length;i++)
		{
			#pragma HLS pipeline
			BRAM0[i]=BRAM1[i];
		}
	}
	else if (mode==3) //BRAM to stream
	{
		for(int i=0;i<length;i++)
		{
			#pragma HLS pipeline
			data.data=BRAM0[i];
			data.dest=dest;
			data.id=0;
			data.user=0;
			OSTREAM<<data;
		}
	}
	else if (mode==4) //stream to BRAM
	{
		for(int i=0;i<length;i++)
		{
			#pragma HLS pipeline
			ISTREAM>>data;
			BRAM0[i]=data.data;
		}
	}
}



void testing_IP1(
	int mode,
	int length,
	int dest,
	ap_uint<128>* BRAM0,
	ap_uint<128>* BRAM1,	
	ap_uint<128>* DDR0,
	ap_uint<128>* DDR1,
	hls::stream<ap_axis<128,U_BITS,TI_BITS,TD_BITS> > &ISTREAM,
	hls::stream<ap_axis<128,U_BITS,TI_BITS,TD_BITS> > &OSTREAM
)
{
	#pragma HLS INTERFACE s_axilite register port=mode
	#pragma HLS INTERFACE s_axilite register port=length
	#pragma HLS INTERFACE s_axilite register port=dest
	
	#pragma HLS interface m_axi port=DDR0 depth=65535 offset=slave bundle=HP0 name=HP0
	#pragma HLS interface m_axi port=DDR1 depth=65535 offset=slave bundle=HP1 name=HP1
	#pragma HLS interface m_axi port=BRAM0 depth=65535 offset=slave bundle=BRAM0 name=BRAM0
	#pragma HLS interface m_axi port=BRAM1 depth=65535 offset=slave bundle=BRAM1 name=BRAM1


	#pragma HLS INTERFACE axis port=ISTREAM name=ISTREAM
	#pragma HLS INTERFACE axis port=OSTREAM	name=OSTREAM
	#pragma HLS INTERFACE s_axilite register port=return

	ap_axis<128,U_BITS,TI_BITS,TD_BITS> data;

	if(mode==0) //DDR to BRAM
	{
		for(int i=0;i<length;i++)
		{
			#pragma HLS pipeline
			BRAM0[i]=DDR0[i];
			BRAM1[i]=DDR1[i];
		}
	}
	else if (mode==1) //BRAM to DDR
	{
		for(int i=0;i<length;i++)
		{
			#pragma HLS pipeline
			DDR0[i]=BRAM0[i];
			DDR1[i]=BRAM1[i];
		}
	}
	else if (mode==2) //BRAM to BRAM
	{
		for(int i=0;i<length;i++)
		{
			#pragma HLS pipeline
			BRAM0[i]=BRAM1[i];
		}
	}
	else if (mode==3) //BRAM to stream
	{
		for(int i=0;i<length;i++)
		{
			#pragma HLS pipeline
			data.data=BRAM0[i];
			data.dest=dest;
			data.id=0;
			data.user=0;
			OSTREAM<<data;
		}
	}
	else if (mode==4) //stream to BRAM
	{
		for(int i=0;i<length;i++)
		{
			#pragma HLS pipeline
			ISTREAM>>data;
			BRAM0[i]=data.data;
		}
	}
}



