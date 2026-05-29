import { SearchResult } from "../types";

interface ResultCardProps {
  item: SearchResult;
}

export default function ResultCard({ item }: ResultCardProps) {
  return (
    <li className="group flex flex-col">
      <span className="mb-1 truncate text-xs text-gray-400">{item.url}</span>

      <a
        href={item.url}
        target="_blank"
        rel="noreferrer"
        className="wrap-break-word text-xl font-medium text-blue-600 decoration-2 group-hover:underline"
      >
        {item.title}
      </a>

      <div className="mt-2 flex items-center gap-3 text-xs text-gray-400">
        <span>
          Relevance:{" "}
          <span className="font-mono text-gray-700">
            {item.score.toFixed(4)}
          </span>
        </span>
        <span className="h-3 w-px bg-gray-200" />
      </div>
    </li>
  );
}
