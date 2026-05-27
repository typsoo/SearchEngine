"use client";

import { useState } from "react";

export default function Home() {
  // We only need to store results now, form inputs are handled by FormData
  const [results, setResults] = useState<string[] | null>(null);

  // React 19 standard: using form actions directly
  const handleSearch = async (formData: FormData) => {
    // Extract values directly from the form submission
    const query = formData.get("query")?.toString();
    const algorithm = formData.get("algorithm")?.toString();

    if (!query?.trim()) return;

    // Placeholder for future backend fetch
    console.log("Fetching data for:", query, "with algorithm:", algorithm);

    // Simulate an API response for testing purposes
    setResults([
      `Result 1 for "${query}" (${algorithm})`,
      `Result 2 for "${query}" (${algorithm})`,
    ]);
  };

  return (
    // Main container takes full height and centers content
    <main className="flex min-h-screen flex-col items-center justify-center p-4">
      {/* The action attribute replaces onSubmit and automatically prevents default reload */}
      <form
        action={handleSearch}
        className="flex w-full max-w-2xl flex-col gap-3 transition-all duration-500 ease-in-out sm:flex-row"
      >
        <input
          type="text"
          name="query"
          placeholder="What are you looking for?"
          className="grow rounded-lg border border-gray-300 px-4 py-3 text-lg shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <select
          name="algorithm"
          defaultValue="tfidf"
          className="rounded-lg border border-gray-300 bg-white px-4 py-3 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="tfidf">TF-IDF</option>
          <option value="bm25">BM25</option>
          <option value="neural">Neural Search</option>
        </select>

        <button
          type="submit"
          className="rounded-lg bg-blue-600 px-6 py-3 font-medium text-white shadow-sm transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Search
        </button>
      </form>

      {/* Render results only if they exist */}
      {results && (
        <div className="mt-8 w-full max-w-2xl">
          <h2 className="mb-4 text-sm text-gray-500">Search results:</h2>
          <ul className="space-y-4">
            {results.map((res, index) => (
              <li
                key={index}
                className="rounded-lg border border-gray-100 p-4 shadow-sm transition-shadow hover:shadow-md"
              >
                {res}
              </li>
            ))}
          </ul>
        </div>
      )}
    </main>
  );
}
