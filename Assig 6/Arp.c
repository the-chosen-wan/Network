#include <netinet/in.h>
#include<errno.h>
#include <sys/socket.h>
#include <stdio.h>
#include <semaphore.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdlib.h>
#include <time.h>
#include <fcntl.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <string.h>
#include <arpa/inet.h>
#define PORT 8000
#define IP 12000

int hash(int x){
    x = ((x >> 15) ^ x) * 0x45d9f3b;
    x = ((x >> 15) ^ x) * 0x45d9f3b;
    x = (x >> 15) ^ x;
    return x;
}

typedef struct{
    int src_ip;
    int src_mac;

    int dst_ip;
    int dst_mac;
}arp;

arp* get_frame(int src_ip,int src_mac,int dst_ip,int dst_mac){
    arp* a = (arp*)malloc(sizeof(arp));
    a->dst_ip=dst_ip;
    a->src_ip=src_ip;
    a->dst_mac=dst_mac;
    a->src_mac=src_mac;
    return a;
}

int main(){
    int n;printf("Enter the number of nodes\n");
    scanf("%d",&n);

    // sem_t *query = sem_open("/query", O_CREAT | O_EXCL, 0666, 1);

    key_t key1 = ftok("shmfile",1);
    key_t key2 = ftok("shmfile",2);

    int* ip2port = (int*)malloc(n*sizeof(int));

    int* ip2ip = (int*)malloc(n*sizeof(int));

    for(int i=0;i<n;i++){
        ip2port[i] = PORT+i;
        ip2ip[i] = IP+i;
    }

    int i=0;
    for(i=0;i<n;i++){
        int id=fork();
        if(id==0)
            break;
    }

    if(i<n&&i!=0){

        int physical = hash(i);
        int sockfd = socket(AF_INET, SOCK_DGRAM,0);
        struct sockaddr_in servaddr;
        struct sockaddr_in recvaddr;
        arp* send = (arp*)malloc(sizeof(arp));arp* recv=(arp*)malloc(sizeof(arp));

        memset(&servaddr,0,sizeof(servaddr));
        servaddr.sin_family=AF_INET;
        servaddr.sin_port = htons(ip2port[i]);
        servaddr.sin_addr.s_addr = inet_addr("127.0.0.2");

        bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr));
        while(1){
            memset(&recvaddr,0,sizeof(recvaddr));

            int len = sizeof(recvaddr);
            recvfrom(sockfd,recv,sizeof(arp),MSG_WAITALL,(struct sockaddr*)&recvaddr,&len);
            printf("Here %d\n",recv->src_ip);
            sleep(1);
            if(recv->dst_ip==-1)
                break;

            if(recv->dst_ip==ip2ip[i]){
                printf("Node %d received required packet\n",i);
                send->dst_ip=recv->dst_ip;send->src_ip=recv->src_ip;
                send->src_mac=recv->src_mac;send->dst_mac=physical;

                sendto(sockfd,(const arp *)send,sizeof(arp),MSG_CONFIRM,(const struct sockaddr*)&recvaddr,len);
            }

            else{
                printf("Arp packet not intended for node %d\n",i);
            }
        }
        
    }
    else if(i==0){
        sleep(1);
        int physical = hash(0);
        int sockfd = socket(AF_INET, SOCK_DGRAM, 0);
        struct sockaddr_in servaddr;
        struct sockaddr_in recvaddr;

        memset(&servaddr, 0, sizeof(servaddr));
        servaddr.sin_family = AF_INET;
        servaddr.sin_addr.s_addr = inet_addr("127.0.0.2");
        servaddr.sin_port=htons(ip2port[0]);

        arp *send = (arp *)malloc(sizeof(arp));
        arp *recv = (arp *)malloc(sizeof(arp));

        bind(sockfd, (const struct sockaddr *)&servaddr, sizeof(servaddr));

        send->dst_mac=-1;send->src_ip=ip2ip[0];send->src_mac=physical;

        while(1){
            int n1;printf("Enter node to query\n");
            scanf("%d",&n1);

            if(n1==0)
                send->dst_ip = -1;
            else
                send->dst_ip=ip2ip[n1];
            
            for(int j=1;j<n;j++){
                servaddr.sin_port=htons(ip2port[j]);
                sendto(sockfd, (const arp *)send,sizeof(arp), MSG_CONFIRM, (const struct sockaddr*)&servaddr, sizeof(servaddr));
                printf("%d\n",errno);
            }

            if(n1==0)
                break;
            
            memset(&recvaddr,0,sizeof(recvaddr));
            int len = sizeof(recvaddr);
            recvfrom(sockfd, recv, sizeof(arp), MSG_WAITALL, (struct sockaddr *)&recvaddr, &len);

            printf("Received back physical address %d\n",recv->dst_mac);
        }
    }
    else
    {
        while (wait(NULL) > 0)
            ;
    }
    return 0;
}