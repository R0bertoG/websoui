Basics
======
The aim of the project is to allow to use the browser in the local computer as an interface to a python program.

This is done using a small python websockets server (server.py), an utilities module (dataformater.py) and a small javascript file (client.js).

This is accomplished by stablishing a websocket connection between a python server and the browser.
The python server have to be initiated with a generator object, every yield of the generator is send by the server to all the open connections. In the case of not opened connections availables the server stop the generator until, at least, one connection is stablished.

An object Queue can be shared by the server and the generator. All the data sent by the browser will be feed to that queue, so all the information sent by the browser can be made available to the generator.

Dependencies
============
python 3
webosockets


Installation
============


.. code:: shell

    git clone https://github.com/R0bertoG/websoui
     
    
