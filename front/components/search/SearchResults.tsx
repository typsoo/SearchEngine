import ResultCard from "@/components/ResultCard";
import type { SearchResult } from "@/types";

interface SearchResponse {
  results: SearchResult[];
  executionTime: number;
}

const algorithmNames: Record<string, string> = {
  custom_tfidf: "Custom TF-IDF",
  custom_bm25: "Custom BM25",
  custom_svd: "Custom TF-IDF with SVD",
  lib_tfidf: "Library TF-IDF with SVD",
  lib_bm25: "Library BM25",
};

async function search(
  query: string,
  algorithm: string,
): Promise<SearchResponse> {
  const appUrl =
    process.env.APP_URL ?? `http://127.0.0.1:${process.env.PORT ?? "3000"}`;
  const url = new URL("/api/search", appUrl);
  url.searchParams.set("q", query);
  url.searchParams.set("algorithm", algorithm);

  const response = await fetch(url, { cache: "no-store" });

  if (!response.ok) {
    throw new Error(`Search request failed with status ${response.status}`);
  }

  return (await response.json()) as SearchResponse;
}

export default async function SearchResults({
  query,
  algorithm,
}: {
  query: string;
  algorithm: string;
}) {
  const data = await search(query, algorithm);

  return (
    <div className="relative z-10 mx-auto w-full pb-36 pt-4 md:max-w-[75%]">
      <div className="mb-6 flex items-center justify-between">
        <h2 className="inline-flex items-center rounded-md bg-blue-100 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-blue-700/10">
          Results found: {data.results.length}
        </h2>
        <h2 className="text-sm font-medium text-gray-500">
          It took: {data.executionTime} ms
        </h2>
        <span className="inline-flex items-center rounded-md bg-blue-100 px-2 py-1 text-xs font-medium text-blue-700 ring-1 ring-blue-700/10">
          {algorithmNames[algorithm] ?? algorithm}
        </span>
      </div>

      <ul className="space-y-6">
        {data.results.map((item) => (
          <ResultCard key={item.id} item={item} />
        ))}
      </ul>
    </div>
  );
}
