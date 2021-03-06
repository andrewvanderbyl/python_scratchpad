"""
Asyncio with RabbitMQ.

Parameters
----------
role (-role or -r): string
    Role for the instance to play.
    Option 1: "start"
    Option 2: "listen"

exchange (-exchange or -e): string
    Name for the RabbitMQ exchange. Can be left as default.

delay(-delay or -d): integer
    Delay (in seconds) that can be applied between responses. This is only to make the interactions
    between the two nodes easier to follow. Default is 3 seconds.

Return: None
"""
import argparse
import asyncio
import aio_pika


async def createConnection(Queue, routing_key, loop):
    """
    Create RabbitMQ Connection.

    Parameters
    ----------
    Queue: List[string]
        Names of queues to create for message exchange.

    routing_key: List[string]
        Names of routing keys to use. In this example it mimics the Queue names.

    loop: Asyncio object
        Asyncio event loop

    Return: [connection, channel, exchange, queueList]
    connection:
        RabbitMQ connection.

    channel:
        Declared channel for use.

    exchange:
        The exchange to use.

    queueList:  List[RabbitMQ queue]
        List of created queues.
    """
    # Create connection
    connection = await aio_pika.connect_robust("amqp://guest:guest@127.0.0.1/", loop=loop)

    # Creating channel
    channel = await connection.channel()

    # Declaring exchange
    exchange = await channel.declare_exchange("direct", auto_delete=True)

    # Declaring queue
    queueList = []
    q_idx = 0
    for q in Queue:
        queue = await channel.declare_queue(q, auto_delete=True)
        await queue.bind(exchange, routing_key[q_idx])
        q_idx += 1
        queueList.append(queue)

    return [connection, channel, exchange, queueList]


async def closeConnection(connection):
    """
    Close RabbitMQ Connection.

    Parameters
    ----------
    connection: RabbitMQ connection
        RabbitMQ connection to close

    Return: None

    """
    await connection.close()


async def _RMQPublish(connection, channel, routing_key, Msg, MsgIdx):
    """
    Rabbitmq Publish.

    Parameters
    ----------
    connection:
        RabbitMQ connection.

    channel:
        Declared channel for use.

    routing_key: List[string]
        Names of routing keys to use. In this example it mimics the Queue names.

    Msg: List[string]
        Message list for publishing

    MsgIdx: int
        Index indicating which message to send next in the sequence

    Return:
    res: Result of publish
        Return the state of the send process.
    """
    res = await channel.default_exchange.publish(aio_pika.Message(body=Msg[MsgIdx].encode()), routing_key=routing_key)
    return res


async def _RMQConsume(connection, channel, queue, routing_key):
    """
    Rabbitmq Consume.

    Parameters
    ----------
    connection:
        RabbitMQ connection.

    channel:
        Declared channel for use.

    queue:  RabbitMQ queue
        queue to listen on.

    routing_key: List[string]
        Names of routing keys to use. In this example it mimics the Queue names.

    Return:
    res: Result of publish
        Return the state of the send process.
    """
    try:
        # Receiving message
        incoming_message = await queue.get(timeout=50)
        # Confirm message
        await incoming_message.ack()

        return incoming_message.body.decode()
    except aio_pika.exceptions.QueueEmpty:
        return None


async def TalkRole(connection, channel, queue, routing_key, TalkMsg, idx, response_delay):
    """
    Talkrole Method.

    Parameters
    ----------
    connection:
        RabbitMQ connection.

    channel:
        Declared channel for use.

    queue:  RabbitMQ queue
        queue to listen on.

    routing_key: List[string]
        Names of routing keys to use. In this example it mimics the Queue names.

    TalkMsg: List[string]
        Message list for publishing

    MsgIdx: int
        Index indicating which message to send next in the sequence

    response_delay: int
        Time in seconds to delay responding. This is only to make the interactions easier to follow.

    Return:
    comms_msg: list[string]
        List of transactional messages for this round
    """
    Node = "Node1"

    Listen = False
    comms_msg = []

    task_Talk = asyncio.create_task(_RMQPublish(connection, channel, routing_key[0], TalkMsg, idx))
    res_talk = await asyncio.gather(task_Talk)

    if res_talk is not None:
        print("\033[1;32;40m" + Node + ":" + TalkMsg[idx])
        Listen = True
        comms_msg.append(TalkMsg[idx])

    while Listen:
        task_ListenRole = asyncio.create_task(_RMQConsume(connection, channel, queue[1], routing_key[1]))
        task_twiddlethumbs = asyncio.create_task(_twiddlethumbs())
        res_listen = await asyncio.gather(task_ListenRole, task_twiddlethumbs)
        comms_msg.append(res_listen[0])

        if res_listen[0] is not None:
            print("\033[1;31;40m" + Node + ":(Msg from Node2): " + res_listen[0])
            Listen = False
            break
    return comms_msg


async def ListenRole(connection, channel, queue, routing_key, ReplyMsg, idx, response_delay):
    """
    Listenrole Method.

    Parameters
    ----------
    connection:
        RabbitMQ connection.

    channel:
        Declared channel for use.

    queue:  RabbitMQ queue
        queue to listen on.

    routing_key: List[string]
        Names of routing keys to use. In this example it mimics the Queue names.

    ReplyMsg: List[string]
        Message list for publishing a reply

    MsgIdx: int
        Index indicating which message to send next in the sequence

    response_delay: int
        Time in seconds to delay responding. This is only to make the interactions easier to follow.

    Return:
        None
    """
    Node = "Node2"

    Listening = True
    comms_msg = []

    while Listening:
        task_ListenRole = asyncio.create_task(_RMQConsume(connection, channel, queue[0], routing_key[0]))
        task_twiddlethumbs = asyncio.create_task(_twiddlethumbs())
        res_listen = await asyncio.gather(task_ListenRole, task_twiddlethumbs)
        comms_msg.append(res_listen[0])

        if res_listen[0] is not None:
            print(Node + ":(Msg from Node1): " + res_listen[0])
            Listening = False
            break

    task_TalkRole = asyncio.create_task(_RMQPublish(connection, channel, routing_key[1], ReplyMsg, idx))
    res_talk = await asyncio.gather(task_TalkRole)
    if res_talk[0] is not None:
        print(Node + ":" + ReplyMsg[idx])
        Listening = True
        comms_msg.append(ReplyMsg[idx])

    return comms_msg


async def _other():
    """
    Other as a separate task.

    Parameters
    ----------
    None

    Return: None
    """
    print("Yay, I'm doing something else!")


async def _twiddlethumbs():
    """
    Twiddle Thumbs as a separate task.

    Parameters
    ----------
    None

    Return: None
    """
    print("Still twiddling thumbs...")


async def main(loop):
    """
    Asyncio main body.

    Parameters
    ----------
    loop: Asyncio Event loop
        Asyncio Event loop

    Return: None
    """
    Queue = ["Queue1", "Queue2"]
    routing_key = Queue
    response_delay = args["delay"]

    TalkMsg = [
        "Hello?",
        "Nice! There is life out there!",
        "I like Easter Eggs!",
        "I like 77, 6F, 6E and 21!",
    ]
    ReplyMsg = [
        "Hello! It's good to hear from you!",
        "What do you like?",
        "Which are your favourite?",
        "Fantastic!",
    ]
    [connection, channel, exchange, queue] = await createConnection(Queue, routing_key, loop)

    for idx in range(len(TalkMsg)):
        if args["role"].lower() == "start":
            task_Start = asyncio.create_task(
                TalkRole(connection, channel, queue, routing_key, TalkMsg, idx, response_delay)
            )
            task_other = asyncio.create_task(_other())
            await asyncio.gather(task_Start, task_other)

        elif args["role"].lower() == "listen":
            task_Listen = asyncio.create_task(
                ListenRole(connection, channel, queue, routing_key, ReplyMsg, idx, response_delay)
            )
            task_other = asyncio.create_task(_other())
            await asyncio.gather(task_Listen, task_other)
        else:
            print("Please enter a role. Options 1) 'start'; 2) 'listen'. ")

    print("\033[1;37;40m Closing Connection")
    await closeConnection(connection)


if __name__ == "__main__":
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--role", type=str, required=True, help="Role to play. Options are 'start' or 'listen'")
    ap.add_argument("-e", "--exchange", type=str, default="", help="RabbitMQ broker")
    ap.add_argument("-d", "--delay", type=int, default=3, help="# response delay")
    args = vars(ap.parse_args())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
