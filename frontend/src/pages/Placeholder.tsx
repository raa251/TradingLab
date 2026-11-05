export function Placeholder({ title }: { title: string }) {
  return (
    <div style={{ padding: "2rem" }}>
      <h1 style={{ fontSize: 24, fontWeight: 700, marginBottom: "0.5rem" }}>{title}</h1>
      <p style={{ color: "var(--text-secondary)" }}>Coming in a future phase.</p>
    </div>
  );
}
