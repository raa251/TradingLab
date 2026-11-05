import { describe, expect, it, vi } from "vitest";

// Unit test – mock fetch and verify api helper behaviour
describe("api helper", () => {
  it("constructs the correct URL for health", async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ status: "ok" }),
    } as Response);
    vi.stubGlobal("fetch", fetchMock);

    const { api } = await import("../lib/api");
    const result = await api.health();

    expect(fetchMock).toHaveBeenCalledWith(
      "/api/v1/health",
      expect.objectContaining({ headers: expect.any(Object) }),
    );
    expect(result.status).toBe("ok");

    vi.unstubAllGlobals();
  });
});
