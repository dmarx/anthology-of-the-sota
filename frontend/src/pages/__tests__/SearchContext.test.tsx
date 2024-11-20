// frontend/src/contexts/search/__tests__/SearchContext.test.tsx
import { render, screen } from '@testing-library/react';
import { useSearch, SearchProvider } from '../SearchContext';
import { Recommendation } from '../../../types/recommendations';

const TestComponent = ({ recommendations }: { recommendations: Recommendation[] }) => {
  const { filterRecommendations, sortRecommendations, state } = useSearch();
  const filtered = filterRecommendations(recommendations);
  const sorted = sortRecommendations(filtered);
  
  return (
    <div>
      <div data-testid="filtered-count">{filtered.length}</div>
      <div data-testid="sorted-first">{sorted[0]?.recommendation}</div>
    </div>
  );
};

const mockRecommendations = [
  {
    id: 'MLR-2023-001',
    recommendation: 'Newer recommendation',
    topic: 'testing',
    status: 'standard',
    source: { paper: 'Test Paper', year: 2023, first_author: 'Test' }
  },
  {
    id: 'MLR-2022-001',
    recommendation: 'Older recommendation',
    topic: 'testing',
    status: 'experimental',
    source: { paper: 'Test Paper', year: 2022, first_author: 'Test' }
  }
];

describe('SearchContext', () => {
  const wrapper = ({ children }: { children: React.ReactNode }) => (
    <SearchProvider>{children}</SearchProvider>
  );

  it('filters by status correctly', () => {
    render(<TestComponent recommendations={mockRecommendations} />, { wrapper });
    expect(screen.getByTestId('filtered-count').textContent).toBe('1'); // Only standard
  });

  it('sorts by newest first by default', () => {
    render(<TestComponent recommendations={mockRecommendations} />, { wrapper });
    expect(screen.getByTestId('sorted-first').textContent).toBe('Newer recommendation');
  });
});
