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
  it('renders with recommendations', () => {
    render(<Home recommendations={mockRecommendations} />);
    
    // Use testid instead of text content
    expect(screen.getByTestId('recommendation-text')).toHaveTextContent('Test recommendation');
  });
});
