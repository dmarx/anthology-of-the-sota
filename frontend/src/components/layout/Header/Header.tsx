// frontend/src/components/layout/Header/Header.tsx
import React from 'react';
import { Filter } from 'lucide-react';
import { SearchBar } from './SearchBar';

interface HeaderProps {
  onSearch: (query: string) => void;
  openFilters: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onSearch, openFilters }) => (
  <header className="sticky top-0 z-50 bg-white border-b shadow-sm">
    <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between gap-4">
      <div className="flex items-center gap-4 flex-1">
        <h1 className="text-xl font-bold text-gray-900 hidden md:block">
          ML Training Recommendations
        </h1>
        <SearchBar onSearch={onSearch} />
      </div>

      <button
        onClick={openFilters}
        className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
      >
        <Filter size={20} />
        <span className="hidden md:inline">Filters</span>
      </button>
    </div>
  </header>
);
