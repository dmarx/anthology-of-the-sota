// frontend/src/contexts/search/SearchContext.tsx
import React, { createContext, useContext, useReducer, useMemo } from 'react';
import type { Recommendation } from '../../types/recommendations';

interface SearchState {
  searchQuery: string;
  topics: string[];
  status: string[];
  sort: 'newest' | 'oldest' | 'topic';
  view: 'grid' | 'list';
}

type SearchAction =
  | { type: 'SET_SEARCH'; query: string }
  | { type: 'TOGGLE_TOPIC'; topic: string }
  | { type: 'TOGGLE_STATUS'; status: string }
  | { type: 'SET_SORT'; sort: SearchState['sort'] }
  | { type: 'SET_VIEW'; view: SearchState['view'] }
  | { type: 'RESET' };

const initialState: SearchState = {
  searchQuery: '',
  topics: [],
  status: ['standard'],
  sort: 'newest',
  view: 'grid'
};

const SearchContext = createContext<{
  state: SearchState;
  dispatch: React.Dispatch<SearchAction>;
  filterRecommendations: (recs: Recommendation[]) => Recommendation[];
  sortRecommendations: (recs: Recommendation[]) => Recommendation[];
} | null>(null);

function searchReducer(state: SearchState, action: SearchAction): SearchState {
  switch (action.type) {
    case 'SET_SEARCH':
      return { ...state, searchQuery: action.query };
    case 'TOGGLE_TOPIC':
      return {
        ...state,
        topics: state.topics.includes(action.topic)
          ? state.topics.filter(t => t !== action.topic)
          : [...state.topics, action.topic]
      };
    case 'TOGGLE_STATUS':
      return {
        ...state,
        status: state.status.includes(action.status)
          ? state.status.filter(s => s !== action.status)
          : [...state.status, action.status]
      };
    case 'SET_SORT':
      return { ...state, sort: action.sort };
    case 'SET_VIEW':
      return { ...state, view: action.view };
    case 'RESET':
      return initialState;
    default:
      return state;
  }
}

export function SearchProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(searchReducer, initialState);

  const filterAndSort = useMemo(() => ({
    filterRecommendations: (recommendations: Recommendation[]) => {
      return recommendations.filter(rec => {
        if (state.searchQuery) {
          const searchRegex = new RegExp(state.searchQuery, 'i');
          const searchableText = [
            rec.recommendation,
            rec.topic,
            rec.source.paper,
            ...(rec.implementations || [])
          ].join(' ');
          
          if (!searchRegex.test(searchableText)) {
            return false;
          }
        }

        if (state.topics.length > 0 && !state.topics.includes(rec.topic)) {
          return false;
        }

        if (state.status.length > 0 && !state.status.includes(rec.status)) {
          return false;
        }

        return true;
      });
    },

    sortRecommendations: (recommendations: Recommendation[]) => {
      return [...recommendations].sort((a, b) => {
        switch (state.sort) {
          case 'newest':
            return b.source.year - a.source.year;
          case 'oldest':
            return a.source.year - b.source.year;
          case 'topic':
            return a.topic.localeCompare(b.topic);
          default:
            return 0;
        }
      });
    }
  }), [state.searchQuery, state.topics, state.status, state.sort]);

  const value = {
    state,
    dispatch,
    ...filterAndSort
  };

  return (
    <SearchContext.Provider value={value}>
      {children}
    </SearchContext.Provider>
  );
}

export function useSearch() {
  const context = useContext(SearchContext);
  if (!context) {
    throw new Error('useSearch must be used within a SearchProvider');
  }
  return context;
}
