import { useCallback, useEffect, useRef, useState } from "react";

const WS_BASE_URL = process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000";

interface UseWebSocketOptions {
  onMessage?: (data: unknown) => void;
  reconnect?: boolean;
}

export function useWebSocket(path: string, options: UseWebSocketOptions = {}) {
  const { onMessage, reconnect = true } = options;
  const wsRef = useRef<WebSocket | null>(null);
  const [connected, setConnected] = useState(false);

  const connect = useCallback(() => {
    const ws = new WebSocket(`${WS_BASE_URL}${path}`);
    wsRef.current = ws;

    ws.onopen = () => setConnected(true);
    ws.onclose = () => {
      setConnected(false);
      if (reconnect) {
        setTimeout(connect, 3000);
      }
    };
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage?.(data);
      } catch {
        onMessage?.(event.data);
      }
    };
  }, [path, onMessage, reconnect]);

  useEffect(() => {
    connect();
    return () => {
      wsRef.current?.close();
    };
  }, [connect]);

  const send = useCallback((data: unknown) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(typeof data === "string" ? data : JSON.stringify(data));
    }
  }, []);

  return { connected, send };
}
