import { useEffect, useState } from "react";
import { api } from "../lib/api";

export function Dashboard() {
  const [status, setStatus] = useState<"loading" | "ok" | "error">("loading");

  useEffect(() => {
    api
      .health()
      .then(() => setStatus("ok"))
      .catch(() => setStatus("error"));
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: "1rem" }}>Dashboard</h1>

      <div
        style={{
          display: "inline-flex",
          alignItems: "center",
          gap: 8,
          padding: "0.5rem 1rem",
          borderRadius: 6,
          background: "var(--bg-panel)",
          border: "1px solid var(--border)",
          fontSize: 13,
        }}
      >
        <span
          style={{
            width: 8,
            height: 8,
            borderRadius: "50%",
            background:
              status === "ok" ? "var(--green)" : status === "error" ? "var(--red)" : "#888",
          }}
        />
        <span style={{ color: "var(--text-secondary)" }}>
          Backend:{" "}
          <span
            style={{
              color:
                status === "ok"
                  ? "var(--green)"
                  : status === "error"
                    ? "var(--red)"
                    : "var(--text-secondary)",
            }}
          >
            {status === "loading" ? "connecting…" : status === "ok" ? "connected" : "not reachable"}
          </span>
        </span>
      </div>

      <div
        style={{
          marginTop: "2rem",
          color: "var(--text-secondary)",
          lineHeight: 1.7,
          maxWidth: 500,
        }}
      >
        <p>Welcome to TradingLab.</p>
        <p style={{ marginTop: "0.5rem" }}>
          Import historical data in the <strong style={{ color: "var(--text-primary)" }}>Data Library</strong>, then
          create a backtest to start replaying market history.
        </p>
      </div>
    </div>
  );
}
