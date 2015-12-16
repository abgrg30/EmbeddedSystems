
/*enum event_type
{
    null,
    motor,
    ultra,
    magneto,
    lcd,    
};*/

//int event_type;

enum priority
{
    low,
    mid,
    high,
};

class event
{
public:
    event()
    {
        type = 0;
        pr = low;
    }
    int type;
    priority pr;
};

event queue_front();
void queue_push(event e);
bool queue_empty();