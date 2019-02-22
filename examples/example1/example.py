import websoui.server as server
import queue
import json
import datetime
import time

def get_sample_generator(received_msgs_queue):
    #The generator should yield any message that we want to pass to
    #the browser. The default behaviour in the browser is to parse
    #a json dictionary. The key in the dictionary is the HTML element
    #where we want to put the information. The content associated to
    #that key is the information.
    while(True):
        #Here we check for a message received from the client:
        if not received_msgs_queue.empty():
            msg = received_msgs_queue.get()
            #If the msg is "STOP" finish the generator and the server will stop.
            if msg == "STOP":
                break
            #Otherwise print the msg and keep going.
            else:
                print(str(msg))
        data_dictionary = {}
        #data_dictionary["span_received_msg"] = str(time.time())
        data_dictionary["span_received_msg"] = str(datetime.datetime.now()
                                                    .strftime("%Y-%m-%d %H:%M:%S"))
        #The generator yield whatever we want to send to the client.
        yield json.dumps(data_dictionary)
        time.sleep(1)

if __name__ == '__main__':
    #A queue object will be used for sending message from the browser to our Python generator object.
    received_msgs_queue = queue.Queue()
    #We pass a reference of the queue to our generator when we create it.
    sample_generator = get_sample_generator(received_msgs_queue)
    #We start the websocket server passing the generator, the queue and the websocket port.
    server.start_websocket_task(sample_generator, received_msgs_queue, 5678)


