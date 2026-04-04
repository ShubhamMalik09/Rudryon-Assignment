import { useEffect, useRef } from "react";

export default function useWebSocket(url, onMessage) {
  const ws = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket(url);

    ws.current.onopen = () => {
      console.log("WS Connected");
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };

    ws.current.onclose = () => {
      console.log("WS Disconnected");
    };

    ws.current.onerror = (err) => {
      console.error("WS Error:", err);
    };

    return () => {
      ws.current.close();
    };
  }, [url]);

  return ws.current;
}