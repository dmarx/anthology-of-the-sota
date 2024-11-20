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

// src/pages/__tests__/index.test.tsx
import { render, screen } from '@testing-library/react';
import Home from '../index';

const mockRecommendations = [
  {
    id: 'MLR-2023-001',
    recommendation: 'Test recommendation',
    topic: 'testing',
    topic_id: 'testing/test',
    status: 'standard',
    source: {
      paper: 'Test Paper',
      paper_id: 'test123',
      year: 2023,
      first_author: 'Test Author'
    }
  }
];

jest.mock('@/contexts/search/SearchContext', () => ({
  SearchProvider: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  useSearch: () => ({
    state: {
      view: 'grid',
      searchQuery: '',
      topics: [],
      status: ['standard']
    },
    filterRecommendations: (recs: any[]) => recs,
    sortRecommendations: (recs: any[]) => recs,
    dispatch: jest.fn()
  })
}));

describe('Home Page', () => {
  it('renders without recommendations', () => {
    render(<Home />);
    expect(screen.getByText('No recommendations match your current filters.')).toBeInTheDocument();
  });

  it('renders with recommendations', () => {
    render(<Home recommendations={mockRecommendations} />);
    expect(screen.getByText('Test recommendation')).toBeInTheDocument();
  });
});

// src/utils/recommendations.test.tsx
import { 
  getRecommendationChain, 
  getRelatedRecommendations,
  groupRecommendationsByTopic 
} from './recommendations';
import type { Recommendation } from '@/types/recommendations';

describe('getRecommendationChain', () => {
  const mockRecommendations: Record<string, Recommendation> = {
    'MLR-2023-001': {
      id: 'MLR-2023-001',
      recommendation: 'Original',
      topic: 'test',
      topic_id: 'test/original',
      superseded_by: 'MLR-2023-002',
      source: {
        paper: 'Test Paper',
        paper_id: 'test123',
        year: 2023,
        first_author: 'Test'
      },
      status: 'deprecated'
    },
    'MLR-2023-002': {
      id: 'MLR-2023-002',
      recommendation: 'Updated',
      topic: 'test',
      topic_id: 'test/updated',
      source: {
        paper: 'Test Paper 2',
        paper_id: 'test456',
        year: 2023,
        first_author: 'Test'
      },
      status: 'standard'
    }
  };

  it('builds recommendation chain', () => {
    const chain = getRecommendationChain(
      mockRecommendations['MLR-2023-001'],
      mockRecommendations
    );
    
    expect(chain).toHaveLength(2);
    expect(chain[0].id).toBe('MLR-2023-001');
    expect(chain[1].id).toBe('MLR-2023-002');
  });
});

describe('getRelatedRecommendations', () => {
  const mockRecommendations: Record<string, Recommendation> = {
    'MLR-2023-001': {
      id: 'MLR-2023-001',
      recommendation: 'First',
      topic: 'test',
      topic_id: 'test/first',
      source: {
        paper: 'Test Paper',
        paper_id: 'test123',
        year: 2023,
        first_author: 'Test'
      },
      status: 'standard'
    },
    'MLR-2023-002': {
      id: 'MLR-2023-002',
      recommendation: 'Second',
      topic: 'test',
      topic_id: 'test/second',
      source: {
        paper: 'Test Paper',
        paper_id: 'test123',
        year: 2023,
        first_author: 'Test'
      },
      status: 'standard'
    }
  };

  it('finds related recommendations by paper', () => {
    const related = getRelatedRecommendations(
      mockRecommendations['MLR-2023-001'],
      mockRecommendations
    );
    
    expect(related).toHaveLength(1);
    expect(related[0].id).toBe('MLR-2023-002');
  });
});

describe('groupRecommendationsByTopic', () => {
  const mockRecommendations: Recommendation[] = [
    {
      id: 'MLR-2023-001',
      recommendation: 'First',
      topic: 'topic1',
      topic_id: 'topic1/first',
      source: {
        paper: 'Test Paper',
        paper_id: 'test123',
        year: 2023,
        first_author: 'Test'
      },
      status: 'standard'
    },
    {
      id: 'MLR-2023-002',
      recommendation: 'Second',
      topic: 'topic2',
      topic_id: 'topic2/second',
      source: {
        paper: 'Test Paper 2',
        paper_id: 'test456',
        year: 2023,
        first_author: 'Test'
      },
      status: 'standard'
    }
  ];

  it('groups recommendations by topic', () => {
    const grouped = groupRecommendationsByTopic(mockRecommendations);
    
    expect(Object.keys(grouped)).toHaveLength(2);
    expect(grouped.topic1).toHaveLength(1);
    expect(grouped.topic2).toHaveLength(1);
    expect(grouped.topic1[0].id).toBe('MLR-2023-001');
    expect(grouped.topic2[0].id).toBe('MLR-2023-002');
  });
});
