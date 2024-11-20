// frontend/src/components/recommendations/ActiveFilters/ActiveFilters.tsx
import React from 'react';
import { X } from 'lucide-react';

interface ActiveFiltersProps {
  topics: string[];
  searchQuery: string;
  onRemoveTopic: (topic: string) => void;
  onClearSearch: () => void;
}

export const ActiveFilters: React.FC<ActiveFiltersProps> = ({
  topics,
  searchQuery,
  onRemoveTopic,
  onClearSearch,
}) => {
  if (topics.length === 0 && !searchQuery) return null;

  return (
    <div className="mb-4 flex flex-wrap gap-2">
      {topics.map(topic => (
        <span
          key={topic}
          className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm flex items-center gap-1"
        >
          {topic}
          <button
            onClick={() => onRemoveTopic(topic)}
            className="hover:text-blue-600"
          >
            <X size={14} />
          </button>
        </span>
      ))}
      {searchQuery && (
        <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm flex items-center gap-1">
          Search: {searchQuery}
          <button
            onClick={onClearSearch}
            className="hover:text-blue-600"
          >
            <X size={14} />
          </button>
        </span>
      )}
    </div>
  );
};
