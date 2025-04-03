"use client"
import { useState } from "react";
import Search from "./components/Search";

type SearchType = "dense" | "sparse" | "hybrid";

interface SearchState {
  query: string;
  results: any[];
  isLoading: boolean;
  error: string | null;
}

export default function Home() {
  const [activeTab, setActiveTab] = useState<SearchType>("dense");
  const [denseState, setDenseState] = useState<SearchState>({
    query: "",
    results: [],
    isLoading: false,
    error: null,
  });
  const [sparseState, setSparseState] = useState<SearchState>({
    query: "",
    results: [],
    isLoading: false,
    error: null,
  });
  const [hybridState, setHybridState] = useState<SearchState>({
    query: "",
    results: [],
    isLoading: false,
    error: null,
  });

  const handleStateChange = (type: SearchType, newState: Partial<SearchState>) => {
    if (type === "dense") {
      setDenseState(prev => ({ ...prev, ...newState }));
    } else if (type === "sparse") {
      setSparseState(prev => ({ ...prev, ...newState }));
    } else {
      setHybridState(prev => ({ ...prev, ...newState }));
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="w-full max-w-2xl">
        <div className="mb-8">
          <div className="border-b border-gray-200 dark:border-gray-700">
            <nav className="-mb-px flex space-x-8">
              <button
                onClick={() => setActiveTab("dense")}
                className={`${
                  activeTab === "dense"
                    ? "border-blue-500 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
              >
                Dense Search
              </button>
              <button
                onClick={() => setActiveTab("sparse")}
                className={`${
                  activeTab === "sparse"
                    ? "border-blue-500 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
              >
                Sparse Search
              </button>
              <button
                onClick={() => setActiveTab("hybrid")}
                className={`${
                  activeTab === "hybrid"
                    ? "border-blue-500 text-blue-600"
                    : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
              >
                Hybrid Search
              </button>
            </nav>
          </div>
        </div>

        <Search 
          type={activeTab}
          state={
            activeTab === "dense"
              ? denseState
              : activeTab === "sparse"
                ? sparseState
                : hybridState
          }
          onStateChange={(newState) => handleStateChange(activeTab, newState)}
        />
      </div>
    </main>
  );
}
