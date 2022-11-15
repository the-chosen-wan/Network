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
#include <pthread.h>
#define MAXPOW 7
#define MAXSEND 16
#define FRAMESIZE 64

char *pad(char *msg)
{
    int len = strlen(msg);
    if (len < FRAMESIZE)
    {
        while (len < FRAMESIZE - 1)
        {
            msg[len] = '0';
            len++;
        }
    }
    msg[len] = '\0';
    return msg;
}

char *unpad(char *msg)
{
    int i = 0;
    while (msg[i] != '0')
        i++;
    msg[i] = '\0';
    return msg;
}

char *itoa(int value, char *result, int base)
{
    // check that the base if valid
    if (base < 2 || base > 36)
    {
        *result = '\0';
        return result;
    }

    char *ptr = result, *ptr1 = result, tmp_char;
    int tmp_value;

    do
    {
        tmp_value = value;
        value /= base;
        *ptr++ = "zyxwvutsrqponmlkjihgfedcba9876543210123456789abcdefghijklmnopqrstuvwxyz"[35 + (tmp_value - value * base)];
    } while (value);

    // Apply negative sign
    if (tmp_value < 0)
        *ptr++ = '-';
    *ptr-- = '\0';
    while (ptr1 < ptr)
    {
        tmp_char = *ptr;
        *ptr-- = *ptr1;
        *ptr1++ = tmp_char;
    }
    return result;
}

void writemsg(int fd[2], char *msg)
{
    int len = strlen(msg) + 1;
    write(fd[1], &len, sizeof(int));
    write(fd[1], msg, len * sizeof(char));
    return;
}

void readmsg(int fd[2], char *buffer)
{
    int len;
    read(fd[0], &len, sizeof(int));
    read(fd[0], buffer, len * sizeof(char));
    return;
}

int main()
{
    printf("Enter number of senders and receivers\n");
    int n;
    scanf("%d", &n);

    char *NAME = (char *)malloc(100 * sizeof(int));
    for (int i = 0; i < n; i++)
    {
        itoa(i, NAME, 10);
        sem_unlink(NAME);
    }

    int ***table;
    table = (int ***)malloc(MAXPOW * sizeof(int **));

    for (int i = 0; i < MAXPOW; i++)
    {
        table[i] = (int **)malloc((1 << i) * sizeof(int *));
        for (int j = 0; j < (1 << i); j++)
            table[i][j] = (int *)malloc((1 << i) * sizeof(int));
    }

    table[0][0][0] = 1;
    for (int i = 1; i < MAXPOW; i++)
    {
        for (int j = 0; j < (1 << i); j++)
        {
            for (int k = 0; k < (1 << i); k++)
            {
                int pow = (1 << (i - 1));
                if (j >= pow && k >= pow)
                    table[i][j][k] = -table[i - 1][j - pow][k - pow];
                else if (j >= pow)
                    table[i][j][k] = table[i - 1][j - pow][k];
                else if (k >= pow)
                    table[i][j][k] = table[i - 1][j][k - pow];
                else
                    table[i][j][k] = table[i - 1][j][k];
            }
        }
    }
    sem_t *semaphores[n];
    for (int i = 0; i < n; i++)
    {
        itoa(i, NAME, 10);
        if (i != 0)
            semaphores[i] = sem_open(NAME, O_CREAT | O_EXCL, 0666, 0);
        else
            semaphores[i] = sem_open(NAME, O_CREAT | O_EXCL, 0666, 1);
    }

    int node_to_channel[n][2];
    int channel_to_node[n][2];

    for (int i = 0; i < n; i++)
    {
        pipe(node_to_channel[i]);
        pipe(channel_to_node[i]);
    }

    int i = 0;
    for (i = 0; i < n; i++)
    {
        int id = fork();
        if (id == 0)
            break;
        else
        {
            printf("Initializing sender %d\n", i + 1);
        }
    }

    if (i == n)
    {
        sleep(1);
        i = 0;
        for (i = 0; i < n; i++)
        {
            int id = fork();
            if (id == 0)
                break;
            else
            {
                printf("Initializing receiver %d\n", i + 1);
            }
        }
        if (i == n)
        {
            char *temp = (char *)malloc(sizeof(char) * FRAMESIZE);
            int *data = (int *)malloc(sizeof(int) * FRAMESIZE * MAXSEND);
            int cnt = 0;
            memset(data, 0, sizeof(int) * FRAMESIZE * MAXSEND);

            for (int j = 0; j < n; j++)
            {
                close(node_to_channel[j][1]);
                close(channel_to_node[j][0]);
            }

            while (1)
            {
                readmsg(node_to_channel[cnt], temp);

                for (int j = 0; j < MAXSEND * FRAMESIZE; j++)
                {
                    data[j] += (temp[j / MAXSEND] * table[4][cnt][j % MAXSEND]);
                }

                cnt = (cnt + 1) % n;
                if (cnt == 0)
                {
                    printf("\nTransmitting\n");
                    sleep(2);
                    for (int j = 0; j < n; j++)
                    {
                        write(channel_to_node[j][1], data, sizeof(int) * FRAMESIZE * MAXSEND);
                    }
                    memset(data, 0, sizeof(int) * FRAMESIZE * MAXSEND);
                }
            }
            for (int j = 0; j < n; j++)
            {
                close(node_to_channel[j][0]);
                close(channel_to_node[j][1]);
            }
        }
        else
        { // Receiver here
            close(channel_to_node[i][1]);
            int *data = (int *)malloc(sizeof(int) * FRAMESIZE * MAXSEND);
            char *msg = (char *)malloc(FRAMESIZE * sizeof(char));
            int *frame = (int *)malloc(sizeof(int) * FRAMESIZE);
            while (1)
            {
                memset(frame, 0, sizeof(int) * FRAMESIZE);
                read(channel_to_node[i][0], data, sizeof(int) * FRAMESIZE * MAXSEND);

                for (int j = 0; j < FRAMESIZE; j++)
                {
                    for (int k = 0; k < MAXSEND; k++)
                        frame[j] += (data[MAXSEND * j + k] * table[4][i][k]);
                }


                for (int j = 0; j < FRAMESIZE; j++)
                    msg[j] = frame[j] / MAXSEND;

                unpad(msg);
                printf("Receiver %d received message %s\n", i + 1, msg);
            }
            close(channel_to_node[i][0]);
        }
    }
    else
    { 
        close(node_to_channel[i][0]);
        char *buffer = (char *)malloc(FRAMESIZE * sizeof(char));

        while (1)
        {
            sleep(3);
            sem_wait(semaphores[i]);
            printf("\nFor node %d enter message\n", i + 1);
            scanf("%s", buffer);
            pad(buffer);
            writemsg(node_to_channel[i], buffer);

            // sem_post(channel);
            sem_post(semaphores[(i + 1) % n]);
        }
    }
    return 0;

    for (int i = 0; i < n; i++)
    {
        itoa(i, NAME, 10);
        sem_unlink(NAME);
    }
    sem_unlink("/channel");
}
