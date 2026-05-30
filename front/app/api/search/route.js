const backendUrl = process.env.SEARCH_API_URL || "http://127.0.0.1:8000";

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get("q")?.trim();
  const algorithm = searchParams.get("algorithm")?.trim();

  if (!query || !algorithm) {
    return Response.json(
      { error: "Both q and algorithm are required" },
      { status: 400 },
    );
  }

  try {
    const response = await fetch(
      `${backendUrl}/api/search?q=${encodeURIComponent(query)}&algorithm=${encodeURIComponent(algorithm)}`,
      { headers: { Accept: "application/json" } },
    );

    if (!response.ok) {
      return Response.json(
        { error: "Search backend request failed" },
        { status: response.status },
      );
    }

    return Response.json(await response.json());
  } catch {
    return Response.json(
      { error: "Search backend is unavailable" },
      { status: 502 },
    );
  }
}
