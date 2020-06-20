#include "op.h"
#include <fstream>
#include <sstream>
#include <string>
#include <iostream>


op_info_t* load_layer_info(
    char* filename)
{
     std::ifstream ifs;
     ifs.open(filename,std::ifstream::in);
       char str[1024];
    op_info_t* head=new op_info_t;

    op_info_t* cur=head;
    op_info_t* prev=head;

    std::string tmp_string;
    std::stringstream linestream;


    ifs.getline(str,1024);
    std::string line(str);
    linestream.str(line);
    while(tmp_string != "scalar_int")
    {
        linestream>>tmp_string;
    }

    int cnt=0;
    while(1)
    {
        std::string line;
        std::getline(ifs,line);
        if(ifs.eof()) break;
        // ifs.getline(str,1024);
  
   

        std::stringstream linestream(line);
        linestream>>cur->op_id;
 

        std::size_t start,end;
        linestream>>tmp_string;
        start=0;
        if(tmp_string !="None")
        {
            while(start<tmp_string.length())
            {
                std::string blobname;
                end=tmp_string.find(",",start+1);
                blobname.assign(tmp_string,start,end-start);
                int dep_id=atoi(blobname.c_str());
                cur->dependence.push_back(dep_id);
                start=end+1;
            }
        }


        linestream>>tmp_string;
        start=0;
        if(tmp_string !="None")
        {
            while(start<tmp_string.length())
            {
                std::string blobname;
                end=tmp_string.find(",",start+1);
                blobname.assign(tmp_string,start,end-start);
                int mem_offset=atoi(blobname.c_str());
                cur->mem_offset_byte.push_back(mem_offset);
                start=end+1;
            }
        }

        linestream>>tmp_string;
        start=0;

        if(tmp_string !="None")
        {
            while(start<tmp_string.length())
            {
                std::string blobname;
                end=tmp_string.find(",",start+1);
                blobname.assign(tmp_string,start,end-start);
                int scalar_int=atoi(blobname.c_str());
                cur->scalar_int.push_back(scalar_int);
                start=end+1;
            }
        }

        prev=cur;
        prev->next=new op_info_t;
        cur=prev->next;
    }

    delete cur;
    prev->next=NULL;

    ifs.close();
    return head;
}
