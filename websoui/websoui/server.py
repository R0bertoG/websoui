import asyncio
import websockets
import os
import types
import queue
import time
import json
#import dataformater
#import numpy as np

def unregistre_websocket(active_websockets, dead_websocket):
    try:
        active_websockets.remove(dead_websocket)
        print("Connection closed. Number of connections: {0}".format(str(len(active_websockets))))
    except KeyError:
        pass

def unregistre_websockets(active_websockets, dead_websockets):
    for websocket in dead_websockets:
        unregistre_websocket(active_websockets, websocket)

#def unregistre_websockets_and_close_event_loop(active_websockets, dead_websockets):
#    unregistre_websockets(active_websockets, dead_websockets)
#    event_loop = asyncio.get_event_loop()
#    event_loop.stop()
    
def create_websocket_consumer(active_websockets, received_msgs_queue):
    #__________________________________________________________
    async def websocket_consumer(websocket, path):
        while(active_websockets):
            try:
                received_msg = await websocket.recv()
            except websockets.exceptions.ConnectionClosed:
                unregistre_websocket(active_websockets, websocket)
                return
            received_msgs_queue.put(received_msg)
    #__________________________________________________________
    return websocket_consumer

def create_websocket_producer(active_websockets, generator):
    #________________________________________________
    async def websocket_producer(websocket, path):
        unactive_websockets = set()
        while(active_websockets):
            try:
                msg = next(generator)
            except StopIteration: 
                print('Generator finished. Clossing the connections...')
                unregistre_websockets(active_websockets, active_websockets)
                #for websocket in active_websockets:
                #    unregistre_websocket(active_websockets, websocket)
            for websocket in active_websockets:
                try:
                    await websocket.send(msg)
                except websockets.exceptions.ConnectionClosed:
                    unactive_websockets.add(websocket)
                    pass
            unregistre_websockets(active_websockets, unactive_websockets)
            #for websocket in unactive_websockets:
            #    unregistre_websocket(active_websockets, websocket)
            unactive_websockets = set()
            await asyncio.sleep(0.001)
    #__________________________________________________
    return websocket_producer

def create_websocket_handler_coroutine(generator, received_msgs_queue):
    if not isinstance(generator, types.GeneratorType):
        raise TypeError("create_websocket_handler_coroutine received " + 
                            str(type(generator))
                            + " as generator parameter"
                            + ". This is not a generator object. Not possible to start websocket server.")

    active_websockets = set()
    websocket_consumer = create_websocket_consumer(active_websockets, received_msgs_queue)
    websocket_producer = create_websocket_producer(active_websockets, generator)
    #__________________________________________________
    async def websocket_handler_coroutine(websocket, path):
        active_websockets.add(websocket)
        print("New connection. Number of connections: {0}".format(str(len(active_websockets))))
        done, pending = await asyncio.wait([
                        websocket_consumer(websocket, path)
                        , websocket_producer(websocket, path)
                            ]
                        , return_when=asyncio.ALL_COMPLETED,)
        
        #event_loop = asyncio.get_event_loop()
        #event_loop.stop()
    #__________________________________________________
    return websocket_handler_coroutine

def start_websocket_task(generator, received_msgs_queue, network_port):
    websocket_server_task = websockets.serve(
            create_websocket_handler_coroutine(generator, received_msgs_queue)
            , 'localhost'
            , network_port)

    print('Websocket server starter in port ' + str(network_port))
    print(str(__file__))
    #print('Point your browser here for client:')
    #print('file://' 
    #        + os.path.dirname(os.path.abspath(__file__))
    #        + '/client.html'
    #        )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(websocket_server_task))
    loop.run_forever()

def generator_test(received_msgs_queue):
    while(True):
        if not received_msgs_queue.empty():
            print('generator says: ' + str( received_msgs_queue.get() ))
        time.sleep(2.25)
        dic = {}
        dic['atextfield'] = str(time.time())
        yield json.dumps(dic)
"""
def generator_test2(received_msgs_queue):
    i = 0
    while(True):
        i += 1;
        yield str(i)

def generator_test3(r):
    dic = {}
    i = 99
    while(True):
        #dic["txtArea"] = str(time.time())
        if i>300:
            i = 99
        i += 1
        plot_data = np.arange(1, i)
        path = 'deer.gif'
        b64img = dataformater.image_file_to_base64(path)
        dic["acanvas"] = b64img;
        yield json.dumps(dic)

def test_t():
    received_msgs_queue = queue.Queue()
    generator = generator_test3(received_msgs_queue)
    for e in generator:
        print(e)
"""

if __name__ == '__main__':
    #start_websocket_task(worldToBrain.get_interaction_generator)
    received_msgs_queue = queue.Queue()
    generator = generator_test(received_msgs_queue)
    start_websocket_task(generator, received_msgs_queue)
    #path = 'deer.gif'
    #b = image_file_to_base64(path)
    #print(b)
    #test_t()
