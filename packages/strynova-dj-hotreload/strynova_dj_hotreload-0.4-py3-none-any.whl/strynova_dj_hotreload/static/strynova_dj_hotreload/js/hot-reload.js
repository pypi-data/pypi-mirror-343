/**
 * Strynova Django Hot Reload Client
 * 
 * This script connects to the hot reload WebSocket server and
 * reloads the page when it receives a reload notification.
 */

(function() {
    // Configuration
    const DEFAULT_WS_HOST = '127.0.0.1';
    const DEFAULT_WS_PORT = 8765;

    // Get configuration from data attributes if available
    const scriptTag = document.currentScript;
    const wsHost = scriptTag.getAttribute('data-ws-host') || DEFAULT_WS_HOST;
    const wsPort = scriptTag.getAttribute('data-ws-port') || DEFAULT_WS_PORT;

    // WebSocket connection
    let socket = null;
    let reconnectAttempts = 0;
    let reconnectTimeout = null;
    let heartbeatInterval = null;
    const HEARTBEAT_INTERVAL = 30000; // 30 seconds
    const CONNECTION_TIMEOUT = 35000; // 35 seconds

    function startHeartbeat() {
        // Clear any existing heartbeat
        stopHeartbeat();

        // Set up heartbeat to detect stale connections
        let lastPongTime = Date.now();

        // Function to check connection and reconnect if needed
        const checkConnection = () => {
            const timeElapsed = Date.now() - lastPongTime;
            if (timeElapsed > CONNECTION_TIMEOUT) {
                console.warn('Connection timeout, reconnecting...');
                socket.close();
                // scheduleReconnect will be called by the close event handler
            } else {
                // Send ping to keep connection alive
                try {
                    if (socket && socket.readyState === WebSocket.OPEN) {
                        socket.send(JSON.stringify({ type: 'ping' }));
                    }
                } catch (error) {
                    console.error('Error sending ping:', error);
                }
            }
        };

        // Start heartbeat interval
        heartbeatInterval = setInterval(checkConnection, HEARTBEAT_INTERVAL);

        // Update lastPongTime when any message is received
        return () => {
            lastPongTime = Date.now();
        };
    }

    function stopHeartbeat() {
        if (heartbeatInterval) {
            clearInterval(heartbeatInterval);
            heartbeatInterval = null;
        }
    }

    function connect() {
        // Close existing socket if any
        if (socket) {
            socket.close();
        }

        // Stop any existing heartbeat
        stopHeartbeat();

        // Create new WebSocket connection
        socket = new WebSocket(`ws://${wsHost}:${wsPort}`);

        // Store the updateLastPongTime function
        let updateLastPongTime;

        // Listen for messages
        socket.addEventListener('message', (event) => {
            try {
                // Update last pong time for any message received
                if (updateLastPongTime) {
                    updateLastPongTime();
                }

                const data = JSON.parse(event.data);

                if (data.action === 'reload') {
                    console.log('Hot reload triggered, reloading page...');
                    window.location.reload();
                }
            } catch (error) {
                console.error('Error processing message:', error);
            }
        });

        // Connection opened
        socket.addEventListener('open', (event) => {
            console.log('Connected to Strynova Hot Reload server');
            reconnectAttempts = 0;

            // Start heartbeat and store the updateLastPongTime function
            updateLastPongTime = startHeartbeat();
            updateLastPongTime(); // Initialize last pong time
        });

        // Connection closed
        socket.addEventListener('close', (event) => {
            console.log('Disconnected from Strynova Hot Reload server');
            stopHeartbeat();
            scheduleReconnect();
        });

        // Connection error
        socket.addEventListener('error', (event) => {
            console.error('WebSocket error:', event);
            stopHeartbeat();
            scheduleReconnect();
        });
    }

    function scheduleReconnect() {
        // Clear any existing reconnect timeout
        if (reconnectTimeout) {
            clearTimeout(reconnectTimeout);
        }

        // Exponential backoff for reconnection attempts
        const delay = Math.min(1000 * Math.pow(1.5, reconnectAttempts), 30000);
        reconnectAttempts++;

        console.log(`Reconnecting in ${delay/1000} seconds...`);
        reconnectTimeout = setTimeout(connect, delay);
    }

    // Initialize connection when the page loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', connect);
    } else {
        connect();
    }
})();
