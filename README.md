A broadcasting server that allows multiple clients to connect then send messages that are broadcasted to all connected clients.

Terminal 1: Start Server by running

                - uv run main.py
                - (broadcast-server) start

Terminal 2: Connect Client 1 by running

                - uv run client.py

Terminal 3: Connect Client 2 by running:

                - uv run client.py

Now you are able to send messages from Terminal 2 and 3 to the Server in Terminal 1, which will be broadcasted to the all the other clients.
