"use client"

type SearchType = "semantic-search" | "lexical-search" | "cascading-retrieval";

interface SearchState {
  query: string;
  results: any[];
  isLoading: boolean;
  error: string | null;
  showSuggestions: boolean;
}

const PROPOSED_QUERIES = [
  "Which games were close?",
  "Which games were competitive?",
  "Which games were hard?",
  "Find games where the home team won?",
  "Who are the strong players for Minnesota Timberwolves?",
  "Find games where rookie players performed well?"
];

interface SearchProps {
  type: SearchType;
  state: SearchState;
  onStateChange: (newState: Partial<SearchState>) => void;
}

export default function Search({ type, state, onStateChange }: SearchProps) {
  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!state.query.trim()) return;

    onStateChange({ error: null, isLoading: true, results: [] });

    try {
      const response = await fetch(`/api/${type}?text_query=${encodeURIComponent(state.query)}`);
      
      if (!response.ok) {
        if (response.status === 422) {
          const errorData = await response.json();
          onStateChange({ 
            error: errorData.detail || "Invalid search query. Please try again.",
            results: [],
            isLoading: false 
          });
          return;
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      onStateChange({ results: data.results, isLoading: false });
    } catch (error) {
      console.error("Search failed:", error);
      onStateChange({ 
        error: "An unexpected error occurred. Please try again.",
        results: [],
        isLoading: false 
      });
    }
  };

  return (
    <div className="w-full">
      <form onSubmit={handleSearch} className="flex gap-2 mb-8">
        <div className="flex-1 relative">
          <input
            type="text"
            value={state.query}
            onChange={(e) => onStateChange({ query: e.target.value })}
            onFocus={() => onStateChange({ showSuggestions: true })}
            onBlur={() => setTimeout(() => onStateChange({ showSuggestions: false }), 200)}
            placeholder="Enter your search query..."
            className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-zinc-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          {state.showSuggestions && (
            <div className="absolute z-10 w-full mt-1 bg-white dark:bg-zinc-800 border border-gray-300 dark:border-gray-700 rounded-lg shadow-lg">
              {PROPOSED_QUERIES.map((query, index) => (
                <div
                  key={index}
                  className="px-4 py-2 hover:bg-gray-100 dark:hover:bg-zinc-700 cursor-pointer"
                  onClick={() => {
                    onStateChange({ query, showSuggestions: false });
                  }}
                >
                  {query}
                </div>
              ))}
            </div>
          )}
        </div>
        <button
          type="submit"
          disabled={state.isLoading || !state.query.trim()}
          className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Search
        </button>
      </form>

      {state.error && (
        <div className="mb-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <p className="text-red-600 dark:text-red-400">{state.error}</p>
        </div>
      )}

      {(state.isLoading || state.results.length > 0) && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">Search Results</h2>
          {state.isLoading ? (
            <div className="flex justify-center items-center py-8">
              <div className="w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin" />
            </div>
          ) : (
            <ul className="space-y-2">
              {state.results.map((result: any) => (
                <li
                  key={result._id}
                  className="p-4 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-zinc-800"
                >
                  <p>ID: {result._id}</p>
                  <p>Score: {result.score}</p>
                  <p>Text: {result.chunk_text}</p>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
} 