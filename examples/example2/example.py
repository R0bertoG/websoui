import websoui.server as server
import websoui.dataformater as dataformater
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
    img_number = 1
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
        data_dictionary["span_received_msg"] = str(datetime.datetime.now()
                                                    .strftime("%Y-%m-%d %H:%M:%S"))

        img_path = 'images/' + str(img_number)  + '.png'
        img_base64 = dataformater.image_file_to_base64(img_path)
        data_dictionary["acanvas"] = img_base64
        #An key in the dictionary without correspondence in the html, should be ignored
        #by the client:
        data_dictionary["test"] = "test content."
        #The generator yield whatever we want to send to the client.
        yield json.dumps(data_dictionary)
        time.sleep(1)
        if img_number > 31:
            img_number = 1
        else:
            img_number += 1

if __name__ == '__main__':
    #It's a good idea to be able to test the generator without the websocket server.
    #The asyncronous aspect of the websocket server make difficult debugging.
    testing = False

    #A queue object will be used for sending message from the browser to our Python generator object.
    received_msgs_queue = queue.Queue()
    #We pass a reference of the queue to our generator when we create it.
    sample_generator = get_sample_generator(received_msgs_queue)
    if testing == False:
        #We start the websocket server passing the generator, the queue and the websocket port.
        server.start_websocket_task(sample_generator, received_msgs_queue, 5678)
    else:
        for sample in sample_generator:
            print(sample)

