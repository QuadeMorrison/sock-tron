# sock-tron
A network browser implementation of [Tron](https://en.wikipedia.org/wiki/Tron).
Play with your friends over the web!

The dependencies for this project are a few years old, so you **must** make
sure you have the right dependencies installed. Run `npm ci` in the client
directory to follow the `package-lock.json` specification. And pip install the
dependencies and versions in `requirements.txt` from the server directory.

## Configuration
Before you can run the project, make sure the configuration files exist. The
example files provide sane defaults, so start by copying those to the
configuration locations:

```bash
cp server/settings.example.py server/settings.py
cp client/settings.example.json client/settings.json
```

## Running the Project
First start the python server:

```bash
cd server
./server.py # python server.py
```

And start the client in a separate session:

```bash
cd client
npm run dev
```

Open up tron in your browser, and you're ready to play!
