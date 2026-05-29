interface SearchBarProps {
  onSubmit: (e: React.SyntheticEvent<HTMLFormElement>) => void;
  currentAlgo: string;
  query: string;
  setQuery: (value: string) => void;
  setAlgo: (value: string) => void;
}

export default function SearchBar({
  onSubmit,
  currentAlgo,
  query,
  setQuery,
  setAlgo,
}: SearchBarProps) {
  return (
    <form
      onSubmit={onSubmit}
      className="group flex w-full items-center rounded-full border border-gray-200 bg-white/95 p-2 shadow-lg transition-all backdrop-blur-sm focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-500/20"
    >
      <input
        type="text"
        name="query"
        required
        value={query ?? ""}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your search query..."
        className="min-w-0 grow bg-transparent px-5 py-3 text-base text-gray-900 outline-none placeholder:text-gray-400"
      />

      <div className="relative flex items-center">
        <select
          name="algorithm"
          value={currentAlgo}
          onChange={(e) => setAlgo(e.target.value)}
          className="appearance-none cursor-pointer bg-transparent py-3 pl-3 pr-7 text-right text-sm font-medium text-gray-700 outline-none transition-colors hover:text-gray-900 focus:text-blue-600"
        >
          <option value="custom_tfidf">Custom TF-IDF</option>
          <option value="custom_bm25">Custom BM25</option>
          <option value="custom_svd">Custom TF-IDF with SVD</option>
          <option value="lib_tfidf">Library TF-IDF with SVD</option>
          <option value="lib_bm25">Library BM25</option>
        </select>

        <div className="pointer-events-none absolute right-2 flex items-center text-gray-400 group-focus-within:text-blue-500">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-4 w-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            strokeWidth={2}
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </div>
      </div>

      <button
        type="submit"
        className="ml-2 shrink-0 rounded-full bg-blue-600 px-7 py-3 text-sm font-medium text-white shadow-sm transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      >
        Search
      </button>
    </form>
  );
}
