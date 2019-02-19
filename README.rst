Basics
======
The aim of the project is to allow to use the browser in the local computer as an interface to a python program.

This a small python websockets server (server.py), an utilities module (dataformater.py) and a small javascript file (client.js).

This is accomplished by stablishing a websocket connection between a python server and the browser.
The python server have to be initiated with a generator object, every yield of the generator is send by the server to all the open connections. In the case of not opened connections availables the server stop the generator until, at least, one connection is stablished.


Dependencies
============
python 3
webosockets


Installation
============


.. code:: shell

    git clone https://github.com/
     
    
