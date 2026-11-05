import type { ReactNode } from "react";
import { NavLink } from "react-router-dom";

const NAV_ITEMS = [
  { to: "/", label: "Dashboard" },
  { to: "/data", label: "Data Library" },
  { to: "/import", label: "Import" },
  { to: "/backtests", label: "Backtests" },
  { to: "/stats", label: "Statistics" },
  { to: "/settings", label: "Settings" },
];

export function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="flex h-full">
      {/* Sidebar */}
      <aside
        style={{
          width: 200,
          background: "var(--bg-secondary)",
          borderRight: "1px solid var(--border)",
          display: "flex",
          flexDirection: "column",
          padding: "1rem 0",
          flexShrink: 0,
        }}
      >
        <div
          style={{
            padding: "0 1rem 1.5rem",
            fontWeight: 700,
            fontSize: 16,
            color: "var(--accent)",
            letterSpacing: "0.05em",
          }}
        >
          TradingLab
        </div>
        <nav style={{ display: "flex", flexDirection: "column", gap: 2 }}>
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              style={({ isActive }) => ({
                padding: "0.5rem 1rem",
                color: isActive ? "var(--accent)" : "var(--text-secondary)",
                background: isActive ? "rgba(88,166,255,0.08)" : "transparent",
                borderLeft: isActive ? "2px solid var(--accent)" : "2px solid transparent",
                textDecoration: "none",
                fontSize: 13,
                fontWeight: isActive ? 600 : 400,
                transition: "all 0.1s",
              })}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </aside>

      {/* Main content */}
      <main style={{ flex: 1, overflow: "auto", display: "flex", flexDirection: "column" }}>
        {children}
      </main>
    </div>
  );
}
