"""Unit test for Asyncio RabbitMQ."""
import Asyncio_rmq
import asyncio
import pytest


@pytest.mark.asyncio
async def test_asyncio_rmq():
    """
    Test Asyncio RMQ Talker and Listener exchange.

    Test Overview:
    --------------
    This test will launch both a Talk (conversation starter) and a Listener (who then replies).
    The exchange goes back and forth four times then concludes. This test checks the send and receive
    messages are as expected.
    Note: a RabbitMQ broker is required to be running for this to work. Using docker, this can be started
    as follows:
        sudo docker run --rm -it --hostname my-rabbi5672:15672 -p 5672:5672 rabbitmq:3-management

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

    ReplyMsg: List[string]
        Message list for publishing a reply

    MsgIdx: int
        Index indicating which message to send next in the sequence

    response_delay: int
        Time in seconds to delay responding. This is only to make the interactions easier to follow.
    """
    Queue = ["Queue1", "Queue2"]
    routing_key = Queue
    response_delay = 0

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

    # Create asyncio event loop
    loop = asyncio.get_event_loop()

    # Create connection
    [connection, channel, exchange, queue] = await Asyncio_rmq.createConnection(Queue, routing_key, loop)

    for idx in range(len(TalkMsg)):
        task_Start = asyncio.create_task(
            Asyncio_rmq.TalkRole(connection, channel, queue, routing_key, TalkMsg, idx, response_delay)
        )

        task_Listen = asyncio.create_task(
            Asyncio_rmq.ListenRole(connection, channel, queue, routing_key, ReplyMsg, idx, response_delay)
        )

        # Launch 'talker' and 'listener'
        task_return = await asyncio.gather(task_Start, task_Listen)

        # print("debug0----------------" + task_return[0][0])
        # print("debug1----------------" + task_return[1][1])

        # Check the outputs are correct
        assert task_return[0][0] == TalkMsg[idx]
        assert task_return[1][1] == ReplyMsg[idx]

    # Close connection
    print("\033[1;37;40m Closing Connection")
    await Asyncio_rmq.closeConnection(connection)
