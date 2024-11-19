// src/components/recommendations/RelatedRecommendations/RelatedRecommendations.test.tsx
import { render, screen } from '@testing-library/react';
import { RelatedRecommendations } from './RelatedRecommendations';

const mockRecommendations = {
  'MLR-2022-001': {
    id: 'MLR-2022-001',
    recommendation: 'First recommendation',
    source: { paper: 'Test Paper' },
    topic: 'optimization'
  },
  'MLR-2022-002': {
    id: 'MLR-2022-002',
    recommendation: 'Second recommendation',
    source: { paper: 'Test Paper' },
    topic: 'attention'
  }
};

describe('RelatedRecommendations', () => {
  it('shows recommendations from same paper', () => {
    render(
      <RelatedRecommendations
        paper="Test Paper"
        recommendations={mockRecommendations}
      />
    );
    
    expect(screen.getByText('First recommendation')).toBeInTheDocument();
    expect(screen.getByText('Second recommendation')).toBeInTheDocument();
    expect(screen.getByText('Other recommendations from this paper')).toBeInTheDocument();
  });

  it('shows recommendations from same topic', () => {
    render(
      <RelatedRecommendations
        topic="optimization"
        recommendations={mockRecommendations}
      />
    );
    
    expect(screen.getByText('First recommendation')).toBeInTheDocument();
    expect(screen.queryByText('Second recommendation')).not.toBeInTheDocument();
    expect(screen.getByText('Related recommendations in this topic')).toBeInTheDocument();
  });
});
