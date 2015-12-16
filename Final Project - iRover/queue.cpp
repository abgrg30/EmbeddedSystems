/*
This Code is for RADAR SYSTEM: QUEUE Implementation.
Course: CSE291E ( Robotics/Embedded Systems)
Assignment: 5
Last Modified: 05-Nov-2015
Team: CodeIT
Developers: Abhinav Garg; Abhijit Tripathi; Pulkit Bhatnagar
University of California, San Diego
*/

#include "queue.h"
#include<queue>
using namespace std;

#define QUEUE_SIZE 50

queue<event> q;
queue<event> p;

bool priorqueue_empty()
{
    return p.empty();
}

bool queue_empty()
{
    return q.empty();
}

event queue_front()
{
    event e;
    
    if(priorqueue_empty())
    {
        if(queue_empty())
        {
            //cout<<endl<<"queue empty!!"<<endl;
        }
        else
        {
            e = q.front();
            q.pop();
        }
    }
    else
    {
        e = p.front();
        p.pop();
    }
    
    return e;
}

void queue_push(event e)
{    
    if(e.pr == high)
    {
        if(p.size() < QUEUE_SIZE)
        {
            p.push(e);
        }
        else
        {
            //cout<<endl<<"priority queue full, event discarded!!"<<endl;
        }
    }
    else
    {
        if(q.size() < QUEUE_SIZE)
        {
            q.push(e);
        }
        else
        {
            //cout<<endl<<"queue full, event discarded!!"<<endl;
        }
    }
}

