// src/components/recommendations/RecommendationCard/RecommendationCard.test.tsx
import { render, screen } from '@testing-library/react';
import { RecommendationCard } from './RecommendationCard';

describe('RecommendationCard', () => {
  const mockRecommendation = {
    id: 'MLR-2022-001',
    recommendation: 'Use flash attention for all attention computations when hardware supports it',
    topic: 'attention',
    status: 'standard',
    source: {
      paper: 'Dao et al. (2022)',
      arxiv_id: '2205.14135',
      year: 2022
    },
    superseded_by: 'MLR-2023-001'
  };

  it('renders basic recommendation information', () => {
    render(
      <RecommendationCard
        recommendation={mockRecommendation}
        allRecommendations={{}}
        onExpand={jest.fn()}
      />
    );

    // Use testids for unique elements
    expect(screen.getByTestId('recommendation-id')).toHaveTextContent('MLR-2022-001');
    expect(screen.getByTestId('recommendation-text')).toHaveTextContent(
      'Use flash attention for all attention computations when hardware supports it'
    );
    expect(screen.getByTestId('recommendation-topic')).toHaveTextContent('attention');
    expect(screen.getByTestId('recommendation-status')).toHaveTextContent('standard');
  });

  it('shows succession chain when recommendation is superseded', () => {
    const allRecommendations = {
      'MLR-2023-001': {
        id: 'MLR-2023-001',
        recommendation: 'New method',
        status: 'standard',
        topic: 'attention',
        source: { paper: 'Paper 2023', year: 2023 }
      }
    };

    render(
      <RecommendationCard
        recommendation={mockRecommendation}
        allRecommendations={allRecommendations}
        onExpand={jest.fn()}
      />
    );

    expect(screen.getByTestId('succession-current')).toHaveTextContent('MLR-2022-001');
    expect(screen.getByTestId('succession-next')).toHaveTextContent('MLR-2023-001');
  });

  it('handles recommendation with no related items', () => {
    const singleRecommendation = {
      id: 'MLR-2022-003',
      recommendation: 'Standalone recommendation',
      topic: 'unique-topic',
      status: 'standard',
      source: { paper: 'Unique Paper', year: 2022 }
    };

    render(
      <RecommendationCard
        recommendation={singleRecommendation}
        allRecommendations={{ 'MLR-2022-003': singleRecommendation }}
        onExpand={jest.fn()}
      />
    );

    expect(screen.queryByTestId('related-recommendations')).not.toBeInTheDocument();
  });
});
