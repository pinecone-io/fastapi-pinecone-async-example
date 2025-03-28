"use client"
import { useState } from "react";

type SearchType = "dense" | "sparse";

interface SearchState {
  query: string;
  results: any[];
  isLoading: boolean;
  error: string | null;
}

interface SearchProps {
  type: SearchType;
  state: SearchState;
  onStateChange: (newState: Partial<SearchState>) => void;
}

export default function Search({ type, state, onStateChange }: SearchProps) {
  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!state.query.trim()) return;

    onStateChange({ error: null, isLoading: true });

    try {
      const response = await fetch(`/api/search/${type}?text_query=${encodeURIComponent(state.query)}`);
      
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
        <input
          type="text"
          value={state.query}
          onChange={(e) => onStateChange({ query: e.target.value })}
          placeholder="Enter your search query..."
          className="flex-1 px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-zinc-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          type="submit"
          disabled={state.isLoading || !state.query.trim()}
          className="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {state.isLoading ? "Searching..." : "Search"}
        </button>
      </form>

      {state.error && (
        <div className="mb-4 p-4 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <p className="text-red-600 dark:text-red-400">{state.error}</p>
        </div>
      )}

      {state.results.length > 0 && (
        <div className="space-y-4">
          <h2 className="text-xl font-semibold mb-4">Search Results</h2>
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
        </div>
      )}
    </div>
  );
} 