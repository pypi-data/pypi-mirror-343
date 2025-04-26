import abc

import websocket


class WebsocketHandler(abc.ABC):
    @abc.abstractmethod
    def on_open(self, ws):
        """Called when the WebSocket connection is opened."""
        pass
    @abc.abstractmethod
    def on_message(self, ws, message):
        """Called when a message is received from the WebSocket."""
        pass
    @abc.abstractmethod
    def on_error(self, ws, error):
        """Called when an error occurs."""
        pass
    @abc.abstractmethod
    def on_close(self, ws):
        """Called when the WebSocket connection is closed."""
        pass
    @abc.abstractmethod
    def on_ping(self, ws, message):
        """Called when a ping message is received."""
        pass
    @abc.abstractmethod
    def on_pong(self, ws, message):
        """Called when a pong message is received."""
        pass
class WebsocketClient:
    def __call__(self, *args, **kwds):
        pass


if __name__ == '__main__':
    ws = websocket.WebSocketApp(
        "ws://127.0.0.1:3300/maner/api/audio/to_text",
        on_open= lambda ws: print("WebSocket opened"),
    )
    ws.run_forever()