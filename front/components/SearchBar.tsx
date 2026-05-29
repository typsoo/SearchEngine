interface SearchBarProps {
  action: (formData: FormData) => void;
  currentAlgo: string;
  query: string;
  setQuery: (value: string) => void;
}

export default function SearchBar({
  action,
  currentAlgo,
  query,
  setQuery,
}: SearchBarProps) {
  return (
    <form action={action} className="flex w-full flex-col gap-3 sm:flex-row">
      <input
        type="text"
        name="query"
        required
        value={query ?? ""}
        placeholder="Enter your search query..."
        onChange={(e) => setQuery(e.target.value)}
        className="grow rounded-xl border border-gray-300 bg-white px-4 py-3 text-base shadow-sm transition-all focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
      />

      <div className="flex gap-2">
        <select
          name="algorithm"
          defaultValue={currentAlgo}
          className="rounded-xl border border-gray-300 bg-white px-3 py-3 text-sm font-medium shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20"
        >
          <option value="custom_tfidf">Custom TF-IDF</option>
          <option value="custom_bm25">Custom BM25</option>
          <option value="custom_svd">Custom TF-IDF with SVD</option>
          <option value="lib_tfidf">Library TF-IDF</option>
          <option value="lib_bm25">Library BM25</option>
        </select>

        <button
          type="submit"
          className="grow rounded-xl bg-blue-600 px-6 py-3 text-sm font-medium text-white shadow-sm transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 sm:grow-0"
        >
          Search
        </button>
      </div>
    </form>
  );
}
