// src/contexts/search/__tests__/SearchContext.test.tsx
import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { SearchProvider, useSearch } from '../SearchContext';
import type { Recommendation } from '@/types/recommendations';

const mockRecommendations: Recommendation[] = [
  {
    id: 'MLR-2023-001',
    recommendation: 'Newer recommendation',
    topic: 'testing',
    topic_id: 'testing/newer',
    status: 'standard',
    source: {
      paper: 'Test Paper 2023',
      paper_id: 'test2023',
      year: 2023,
      first_author: 'Test'
    }
  }
];

const TestComponent: React.FC<{ recommendations: Recommendation[] }> = ({ recommendations }) => {
  const { state, dispatch, filterRecommendations, sortRecommendations } = useSearch();
  
  const filtered = filterRecommendations(recommendations);
  const sorted = sortRecommendations(filtered);
  
  return (
    <div>
      <div data-testid="search-query">{state.searchQuery}</div>
      <div data-testid="view-mode">{state.view}</div>
      <div data-testid="filtered-count">{filtered.length}</div>
      <div data-testid="sorted-first">{sorted[0]?.recommendation}</div>
      
      <button 
        onClick={() => dispatch({ type: 'SET_SEARCH', query: 'test' })}
        data-testid="set-search"
      >
        Set Search
      </button>
      
      <button
        onClick={() => dispatch({ type: 'TOGGLE_TOPIC', topic: 'testing' })}
        data-testid="toggle-topic"
      >
        Toggle Topic
      </button>

      <button
        onClick={() => dispatch({ type: 'SET_VIEW', view: 'list' })}
        data-testid="set-view"
      >
        Set View
      </button>
    </div>
  );
};

describe('SearchContext', () => {
  const wrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => (
    <SearchProvider>{children}</SearchProvider>
  );

  it('provides initial state', () => {
    render(<TestComponent recommendations={mockRecommendations} />, { wrapper });
    
    expect(screen.getByTestId('search-query')).toHaveTextContent('');
    expect(screen.getByTestId('view-mode')).toHaveTextContent('grid');
    expect(screen.getByTestId('filtered-count')).toHaveTextContent('1');
  });

  it('filters by search query', () => {
    render(<TestComponent recommendations={mockRecommendations} />, { wrapper });
    
    fireEvent.click(screen.getByTestId('set-search'));
    expect(screen.getByTestId('search-query')).toHaveTextContent('test');
    expect(screen.getByTestId('filtered-count')).toHaveTextContent('1');
  });

  it('changes view mode', () => {
    render(<TestComponent recommendations={mockRecommendations} />, { wrapper });
    
    fireEvent.click(screen.getByTestId('set-view'));
    expect(screen.getByTestId('view-mode')).toHaveTextContent('list');
  });

  it('handles empty recommendations', () => {
    render(<TestComponent recommendations={[]} />, { wrapper });
    expect(screen.getByTestId('filtered-count')).toHaveTextContent('0');
  });
});
