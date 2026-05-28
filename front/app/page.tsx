"use client";

import { useState } from "react";
import SearchBar from "@/components/SearchBar";
import ResultCard from "@/components/ResultCard";
import { SearchResult } from "@/types";

export default function Home() {
  const [results, setResults] = useState<SearchResult[] | null>(null);
  const [time, setTime] = useState<number | null>(null);

  const [currentAlgo, setCurrentAlgo] = useState("tfidf");

  const handleSearch = async (formData: FormData) => {
    const query = formData.get("query")?.toString();
    const algorithm = formData.get("algorithm")?.toString() || "tfidf";

    if (!query?.trim()) return;

    setCurrentAlgo(algorithm);

    try {
      const backendUrl = `http://127.0.0.1:8000/api/search?q=${encodeURIComponent(query)}&algorithm=${algorithm}`;

      const response = await fetch(backendUrl, {
        method: "GET",
        headers: {
          Accept: "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`Server responded with status: ${response.status}`);
      }

      const { results: data, executionTime } = (await response.json()) as {
        results: SearchResult[];
        executionTime: number;
      };

      setTime(executionTime);
      setResults(data);
    } catch (error) {
      console.error("Data transfer failed:", error);
      setResults([]);
    }
  };

  const hasResults = results !== null;

  return (
    <main
      className={`flex min-h-screen flex-col bg-white transition-all duration-500 p-4 ${hasResults ? "justify-start" : "justify-center"}`}
    >
      {hasResults && (
        <div className="mx-auto w-full max-w-2xl animate-fade-in pb-28 pt-4">
          <div className="mb-6 flex items-center justify-between border-b border-gray-100 pb-3">
            <h2 className="text-sm font-medium text-gray-500">
              Results found: {results.length}
            </h2>
            <h2 className="text-sm font-medium text-gray-500">
              It took: {time}
            </h2>
            <span className="inline-flex items-center rounded-md bg-blue-50 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-blue-750/10">
              Algorithm: {currentAlgo.toUpperCase()}
            </span>
          </div>

          <ul className="space-y-6">
            {results.map((item) => (
              <ResultCard key={item.id} item={item} />
            ))}
          </ul>
        </div>
      )}

      <div
        className={`mx-auto w-full max-w-2xl ${
          hasResults
            ? "fixed bottom-0 left-0 right-0 max-w-full border-t border-gray-100 bg-white/80 p-4 backdrop-blur-md"
            : "relative"
        }`}
      >
        <div className={hasResults ? "mx-auto max-w-2xl" : ""}>
          <SearchBar action={handleSearch} currentAlgo={currentAlgo} />
        </div>
      </div>
    </main>
  );
}
