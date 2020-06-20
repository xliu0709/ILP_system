#include <pthread.h>

 
#include <vector>
#include <stdio.h>
#include <unistd.h>
#include <time.h>    
#include "op.h"
#include "parser.h"

bool done[1024];
#define IP_NUMBER 3

pthread_rwlock_t RW_MUTEX; 




void *ip_execution(void *op_head)
{
    op_info_t* cur_op= (op_info_t*) op_head;
    time_t rawtime;
    struct tm * timeinfo;
    while(cur_op!=NULL)
    {
        // depdency check
        while(1)
        {
            bool dependence_fufill=true;
            pthread_rwlock_rdlock(& RW_MUTEX);
            for(std::vector<int>::iterator dep_idx = cur_op->dependence.begin() ; dep_idx != cur_op->dependence.end(); ++dep_idx)
            {
                if(!done[*dep_idx]) dependence_fufill=false;   
            }
            pthread_rwlock_unlock(& RW_MUTEX);
            if(dependence_fufill) break;
        }
        time (&rawtime);
        timeinfo = localtime (&rawtime);
     

        printf("Start op %d at %s\n", cur_op->op_id,  asctime(timeinfo));
        // IP deployment (dummy)
        sleep(5);
        time (&rawtime);
        timeinfo = localtime (&rawtime);
        printf("End op %d at %s\n", cur_op->op_id,  asctime(timeinfo));

        // operation status update
        pthread_rwlock_wrlock(& RW_MUTEX);
        done[cur_op->op_id]=true;
        pthread_rwlock_unlock(& RW_MUTEX);
        
        cur_op=cur_op->next;
    }
    pthread_exit((void*) 0);
}



void free_op_chain( 
    op_info_t* head
)
{
    op_info_t* next;
    op_info_t* cur;
    cur=head;
    
    while(cur!=NULL)
    {
        next=cur->next;
        delete cur;
        cur=next;
    }
}


int main()
{   
    op_info_t* op_queues[IP_NUMBER];
    op_queues[0]=load_layer_info("op0.csv");
    op_queues[1]=load_layer_info("op1.csv");
    

    pthread_attr_t attr;
    pthread_t thread[IP_NUMBER];
    void* status;

    pthread_attr_init(&attr);
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);

   for(int t=0; t<2; t++) {
       printf("Main: creating thread %ld\n", t);
       bool rc = pthread_create(&thread[t], &attr, ip_execution, (void *) (op_queues[t]) );  
       if (rc) {
          printf("ERROR; return code from pthread_create() is %d\n", rc);
          exit(-1);
          }
       }
    pthread_attr_destroy(&attr);
    for(int t=0; t<2; t++) {
       bool rc = pthread_join(thread[t], &status);
       if (rc) {
          printf("ERROR; return code from pthread_join() is %d\n", rc);
          exit(-1);
          }
       printf("Main: completed join with thread %ld having a status of %ld\n",t,(long)status);
       }

    // op_info_t* cur=op_queues[1];
    // while(cur!=NULL)
    // {
    //     std::cout<<"op_id:"<<cur->op_id<<std::endl;
    //     std::cout<<"depedence:"<<std::endl;
    //     for(int i=0;i<cur->dependence.size();i++)
    //     {
    //         std::cout<<cur->dependence[i]<<" ";
    //     }
    //     std::cout<<std::endl;
    //     cur=cur->next;
    // }

free_op_chain(op_queues[1]);

free_op_chain(op_queues[0]);

}