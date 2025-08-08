# PYctochat

This application is a recreation of the HIT Nintendo DS messaging program known as, "Pictochat" using Tkinter and Pygame.


## Authors

- [@AkuraEx](https://github.com/AkuraEx) - Andrew Walters
- [@underclockd](https://github.com/underclockd) - Aiden Brown

## Screenshots

![App Screenshot](https://raw.githubusercontent.com/AkuraEx/PYctochat/refs/heads/main/assets/awesomeScreenshot1.png)

![App Screenshot 2](https://raw.githubusercontent.com/AkuraEx/PYctochat/refs/heads/main/assets/awesomeScreenshot2.png)


## Dependencies
- LibP2P
- Multiaddr
- Pillow
- Pygame
- Pyglet
- Tkinter
- Trio


## How To Run

There are 4 command line arguments:
- -d: Destination
- -n: Username
- -c: Color Theme
- -p: Port

### Example Usage:

First player will be the server and specify the port.
In the main directory type:
```bash
  python main.py -p 8000 -n {any name here} -c {red, blue, or green}
```

You will receive a message in the terminal saying:
```bash
Run this from the same folder in another console:
python main.py -d /ip4/0.0.0.0/tcp/8000/p2p/QmSKvN1kfGxQjMTHGHHRQTvgxpKnUwK8ksyqc8ULjokEHZ    
```

The string of chracters after p2p will be different every time

The second player will take that command and run in another console to connect:

```bash
python main.py -d /ip4/0.0.0.0/tcp/8000/p2p/QmSKvN1kfGxQjMTHGHHRQTvgxpKnUwK8ksyqc8ULjokEHZ    
-n {any name here} -c {red, blue, or green}
```

If you wish to run to program without a second user you can simply run:
```bash
python main.py
```
    