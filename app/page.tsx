"use client"
import { useState } from "react";
import Search from "./components/Search";

type SearchType = "semantic-search" | "lexical-search" | "cascading-retrieval";

interface SearchState {
  query: string;
  results: any[];
  isLoading: boolean;
  error: string | null;
}

export default function Home() {
  const [activeTab, setActiveTab] = useState<SearchType>("semantic-search");
  const [semanticSearchState, setSemanticSearchState] = useState<SearchState>({
    query: "",
    results: [],
    isLoading: false,
    error: null,
  });
  const [lexicalSearchState, setLexicalSearchState] = useState<SearchState>({
    query: "",
    results: [],
    isLoading: false,
    error: null,
  });
  const [cascadingRetrievalState, setCascadingRetrievalState] = useState<SearchState>({
    query: "",
    results: [],
    isLoading: false,
    error: null,
  });

  const handleStateChange = (type: SearchType, newState: Partial<SearchState>) => {
    if (type === "semantic-search") {
      setSemanticSearchState(prev => ({ ...prev, ...newState }));
    } else if (type === "lexical-search") {
      setLexicalSearchState(prev => ({ ...prev, ...newState }));
    } else {
      setCascadingRetrievalState(prev => ({ ...prev, ...newState }));
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="w-full max-w-2xl">
        <div className="mb-8">
          <div className="border-b border-gray-200 dark:border-gray-700">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab("semantic-search")}
                className={`${
                  activeTab === "semantic-search"
                    ? "border-blue-500 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
              >
                Semantic Search
              </button>
              <button
                onClick={() => setActiveTab("lexical-search")}
                className={`${
                  activeTab === "lexical-search"
                    ? "border-blue-500 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
              >
                Lexical Search
              </button>
              <button
                onClick={() => setActiveTab("cascading-retrieval")}
                className={`${
                  activeTab === "cascading-retrieval"
                    ? "border-blue-500 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
              >
                Cascading Retrieval
              </button>
            </nav>
          </div>
        </div>

        <Search 
          type={activeTab}
          state={
            activeTab === "semantic-search"
              ? semanticSearchState
              : activeTab === "lexical-search"
                ? lexicalSearchState
                : cascadingRetrievalState
          }
          onStateChange={(newState) => handleStateChange(activeTab, newState)}
        />
      </div>
    </main>
  );
}
