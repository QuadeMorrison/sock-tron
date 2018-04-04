# sock-tron
A network browser implementation of tron. Play with your friends over the web!

To run on your system, first make sure vue is installed. You also need socketio
for python 3. Next run these commands (in the root directory of the repo).

```bash
cp server/settings.example.py server/settings.py
cp client/settings.example.json client/settings.json
./server.py # python server.py
```

Edit the setting files to your heart's content. You may want to pay special
attention to the port numbers.

Now open a new terminal window and start the python server.
```bash
cd server
./server.py # python server.py
```

And you need another terminal window to run the client.
```bash
cd client
npm i
npm run dev
```
Open it in your browser and... Mwala! You have a tron server up and running! Be
sure to play with friends.
