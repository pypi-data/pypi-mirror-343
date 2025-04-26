import asyncio
import json
import threading
import websockets
from typing import Set, Dict, Any, Optional

class HotReloadWebSocketServer:
    """
    WebSocket server that notifies connected clients when files change.
    """
    def __init__(self, host: str = '127.0.0.1', port: int = 8765):
        """
        Initialize the WebSocket server.

        Args:
            host: Host to bind the server to
            port: Port to bind the server to
        """
        self.host = host
        self.port = port
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        self.server = None
        self.thread = None
        self.running = False

    async def _register(self, websocket: websockets.WebSocketServerProtocol):
        """Register a new client connection."""
        self.clients.add(websocket)
        print(f"Client connected. Total clients: {len(self.clients)}")

    async def _unregister(self, websocket: websockets.WebSocketServerProtocol):
        """Unregister a client connection."""
        self.clients.remove(websocket)
        print(f"Client disconnected. Total clients: {len(self.clients)}")

    async def _handler(self, websocket: websockets.WebSocketServerProtocol):
        """Handle a client connection."""
        await self._register(websocket)
        try:
            async for message in websocket:
                # Handle messages from clients
                try:
                    data = json.loads(message)

                    # Handle ping messages with a pong response
                    if data.get('type') == 'ping':
                        try:
                            await websocket.send(json.dumps({'type': 'pong'}))
                        except Exception as e:
                            print(f"Error sending pong response: {e}")
                    else:
                        print(f"Received message from client: {data}")
                except json.JSONDecodeError:
                    print(f"Received non-JSON message from client: {message}")
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self._unregister(websocket)

    async def _send_to_all(self, message: Dict[str, Any]):
        """Send a message to all connected clients."""
        if not self.clients:
            return

        json_message = json.dumps(message)

        # Send to each client individually with error handling
        for client in list(self.clients):
            try:
                await client.send(json_message)
            except Exception as e:
                print(f"Error sending message to client: {e}")
                # Client might be disconnected, try to unregister it
                try:
                    await self._unregister(client)
                except Exception:
                    # If unregister fails, just remove it from the set
                    self.clients.discard(client)

    def notify_reload(self):
        """Notify all clients to reload the page."""
        if not self.running:
            return

        message = {"action": "reload"}

        # Create a new event loop for the current thread if needed
        try:
            loop = asyncio.get_event_loop()
            was_running = True
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            was_running = False

        # Always use run_until_complete which is safer across different threads
        try:
            # Create a new task for sending the message
            task = loop.create_task(self._send_to_all(message))

            # Wait for the task to complete without closing the loop
            loop.run_until_complete(task)
        except Exception as e:
            print(f"Error sending reload notification: {e}")

        # Don't close the loop as it might be used by other parts of the code

        print(f"Sent reload notification to {len(self.clients)} clients")

    async def _run_server(self):
        """Run the WebSocket server."""
        self.server = await websockets.serve(self._handler, self.host, self.port)
        print(f"WebSocket server started at ws://{self.host}:{self.port}")
        await self.server.wait_closed()

    def _run_in_thread(self):
        """Run the WebSocket server in a separate thread."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(self._run_server())
        except Exception as e:
            print(f"WebSocket server error: {e}")
        finally:
            loop.close()

    def start(self):
        """Start the WebSocket server in a separate thread."""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_in_thread, daemon=True)
        self.thread.start()

    def stop(self):
        """Stop the WebSocket server."""
        if not self.running:
            return

        self.running = False

        # Create a new event loop for the current thread if needed
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if self.server:
            self.server.close()
            loop.run_until_complete(self.server.wait_closed())

        if self.thread:
            self.thread.join(timeout=1.0)
            self.thread = None

        print("WebSocket server stopped.")
