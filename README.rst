Basics
======
The aim of the project is to allow to use the browser in the local computer as an easy to use interface to a python program.

This is done using a small python websockets server (server.py), an utilities module (dataformater.py) and a small javascript file (client.js).

This is accomplished by stablishing a websocket connection between a python server and the browser.
The python server have to be initiated with a generator object (https://wiki.python.org/moin/Generators), every yield of the generator is send by the server to all the open connections. In the case of not opened connections availables the server stop the generator until, at least, one connection is stablished.

An object Queue (https://docs.python.org/2/library/queue.html) can be shared by the server and the generator. All the data sent by the browser will be feed to that queue, so all the information sent by the browser can be made available to the generator.

Dependencies
============
- python 3.6.8
- websockets (https://pypi.org/project/websockets/)


Installation
============

.. code:: shell

    git clone https://github.com/R0bertoG/websoui
    cd websoui/websoui
    python setup.py install 

How it works
============
The server consume a generator, it's in this generator where the functionality that we wish should be implemented.
The generator do whatever it's necessary and **yield** what should be show in the UI.
Besides de generator, the server is started with a queue object and the port number for the websocket.

.. code:: python

    websoui.server.start_websocket_task(my_generator, received_msgs_queue, 5678)

Even if the server will send everything that the generator yield, the idea is to send a json dictionary where the key of the dictionary will be the DOM element that will receive the data. The content of the dictionary is the data.


.. code:: python
   
        data_dictionary = {}
        data_dictionary['html_id']="hello world"
        yield json.dumps(data_dictionary)

If we import the javascript code in our HTML and we start the websocket client like this:

	<script src="client.js"></script>

        <script>
	    wsclient.start_connection('ws://127.0.0.1:5678/');
        </script>



The javascript client will search automatically for a DOM object with ID 'html_id' and will try to show the content in it. 

At the moment, only SPAN, TEXTAREA, INPUT and CANVAS elements are supported. 
