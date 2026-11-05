import { BrowserRouter, Route, Routes } from "react-router-dom";
import { Layout } from "./components/Layout";
import { Dashboard } from "./pages/Dashboard";
import { Placeholder } from "./pages/Placeholder";

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/data" element={<Placeholder title="Data Library" />} />
          <Route path="/import" element={<Placeholder title="Import" />} />
          <Route path="/backtests" element={<Placeholder title="Backtests" />} />
          <Route path="/stats" element={<Placeholder title="Statistics" />} />
          <Route path="/settings" element={<Placeholder title="Settings" />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
