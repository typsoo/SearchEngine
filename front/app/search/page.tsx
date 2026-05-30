import { Suspense } from "react";
import SearchBar from "@/components/search/SearchBar";
import SearchResults from "@/components/search/SearchResults";

interface SearchPageProps {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}

function SearchResultsSkeleton() {
  return (
    <div className="relative z-10 mx-auto w-full space-y-6 pt-4 md:max-w-[75%]">
      <div className="mb-6 flex items-center justify-between border-b border-gray-200 pb-3">
        <div className="h-4 w-32 animate-pulse rounded bg-gray-200" />
        <div className="h-4 w-20 animate-pulse rounded bg-gray-200" />
        <div className="h-6 w-32 animate-pulse rounded-md bg-gray-200" />
      </div>
      <div className="space-y-6">
        {Array.from({ length: 5 }, (_, index) => (
          <div key={index} className="space-y-2">
            <div className="h-3 w-1/3 animate-pulse rounded bg-gray-200" />
            <div className="h-6 w-2/3 animate-pulse rounded bg-gray-200" />
            <div className="h-3 w-24 animate-pulse rounded bg-gray-200" />
          </div>
        ))}
      </div>
    </div>
  );
}

export default async function SearchPage({ searchParams }: SearchPageProps) {
  const params = await searchParams;
  const query = typeof params.q === "string" ? params.q.trim() : "";
  const algorithm =
    typeof params.algorithm === "string" ? params.algorithm : "custom_tfidf";

  return (
    <main className="relative flex min-h-screen flex-col p-4">
      {" "}
      {query && (
        <Suspense
          key={JSON.stringify([query, algorithm])}
          fallback={<SearchResultsSkeleton />}
        >
          <SearchResults query={query} algorithm={algorithm} />
        </Suspense>
      )}
      <div
        className={`mx-auto w-full ${
          query
            ? "fixed bottom-0 left-0 right-0 z-20 max-w-full bg-transparent p-6"
            : "relative z-10 max-w-2xl"
        }`}
      >
        <div className={query ? "mx-auto w-full md:max-w-[75%]" : ""}>
          <SearchBar
            key={JSON.stringify([query, algorithm])}
            defaultAlgorithm={algorithm}
            defaultQuery={query}
          />
        </div>
      </div>
    </main>
  );
}
