"use client";

import { useState } from "react";
import SearchBar from "@/components/SearchBar";
import ResultCard from "@/components/ResultCard";
import WelcomeText from "./WelcomeText";
import MorphingBackground from "./MorphingBackground";
import { SearchResult } from "@/types";

export default function SearchSection() {
  const [results, setResults] = useState<SearchResult[] | null>(null);
  const [time, setTime] = useState<number | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  const [dropdownAlgo, setDropdownAlgo] = useState("custom_tfidf");
  const [appliedAlgo, setAppliedAlgo] = useState("custom_tfidf");

  const handleSearch = async (e: React.SyntheticEvent<HTMLFormElement>) => {
    e.preventDefault();

    const formData = new FormData(e.currentTarget);
    const query = formData.get("query")?.toString();

    const algorithm = formData.get("algorithm")?.toString() || dropdownAlgo;

    if (!query?.trim()) return;

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

      setAppliedAlgo(algorithm);
    } catch (error) {
      console.error("Data transfer failed:", error);
      setResults([]);
    }
  };

  const hasResults = results !== null;

  return (
    <div
      className={`relative flex min-h-screen flex-col bg-slate-50 transition-all duration-500 p-4 ${hasResults ? "justify-start" : "justify-center"}`}
    >
      <MorphingBackground />

      {hasResults && (
        <div className="relative z-10 mx-auto w-full md:max-w-[75%] pb-36 pt-4">
          <div className="mb-6 flex items-center justify-between border-b border-gray-200 pb-3">
            <h2 className="text-sm font-medium text-gray-500">
              Results found: {results.length}
            </h2>
            <h2 className="text-sm font-medium text-gray-500">
              It took: {time} ms
            </h2>
            <span className="inline-flex items-center rounded-md bg-blue-100 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-blue-700/10">
              Algorithm: {appliedAlgo.toUpperCase()}
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
        className={`mx-auto w-full ${
          hasResults
            ? "fixed bottom-0 left-0 right-0 z-20 max-w-full bg-transparent p-6"
            : "relative z-10 max-w-2xl"
        }`}
      >
        {!hasResults && <WelcomeText />}

        <div className={hasResults ? "mx-auto w-full md:max-w-[75%]" : ""}>
          <SearchBar
            onSubmit={handleSearch}
            currentAlgo={dropdownAlgo}
            setAlgo={setDropdownAlgo}
            query={searchQuery}
            setQuery={setSearchQuery}
          />
        </div>
      </div>
    </div>
  );
}
