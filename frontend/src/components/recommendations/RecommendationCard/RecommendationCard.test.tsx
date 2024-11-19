// src/components/recommendations/RecommendationCard/RecommendationCard.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { RecommendationCard } from './RecommendationCard';

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

const mockAllRecommendations = {
  'MLR-2022-001': mockRecommendation,
  'MLR-2023-001': {
    id: 'MLR-2023-001',
    recommendation: 'Use flash attention 2.0',
    topic: 'attention',
    status: 'standard',
    source: {
      paper: 'Dao et al. (2023)',
      arxiv_id: '2307.08691',
      year: 2023
    }
  }
};

const mockOnExpand = jest.fn();

describe('RecommendationCard', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders basic recommendation information', () => {
    render(
      <RecommendationCard
        recommendation={mockRecommendation}
        allRecommendations={mockAllRecommendations}
        onExpand={mockOnExpand}
      />
    );

    // Check basic content
    expect(screen.getByText('MLR-2022-001')).toBeInTheDocument();
    expect(screen.getByText('Use flash attention for all attention computations when hardware supports it')).toBeInTheDocument();
    expect(screen.getByText('attention')).toBeInTheDocument();
    expect(screen.getByText('standard')).toBeInTheDocument();
    expect(screen.getByText('Dao et al. (2022)')).toBeInTheDocument();
  });

  it('renders arXiv link when arxiv_id is provided', () => {
    render(
      <RecommendationCard
        recommendation={mockRecommendation}
        allRecommendations={mockAllRecommendations}
        onExpand={mockOnExpand}
      />
    );

    const arxivLink = screen.getByRole('link');
    expect(arxivLink).toHaveAttribute('href', 'https://arxiv.org/abs/2205.14135');
  });

  it('shows succession chain when recommendation is superseded', () => {
    render(
      <RecommendationCard
        recommendation={mockRecommendation}
        allRecommendations={mockAllRecommendations}
        onExpand={mockOnExpand}
      />
    );

    // Verify both recommendations appear in the succession chain
    expect(screen.getByText('MLR-2022-001')).toBeInTheDocument();
    expect(screen.getByText('MLR-2023-001')).toBeInTheDocument();
    expect(screen.getByText('Recommendation Evolution')).toBeInTheDocument();
  });

  it('shows related recommendations from same paper', () => {
    const multipleRecsFromSamePaper = {
      ...mockAllRecommendations,
      'MLR-2022-002': {
        id: 'MLR-2022-002',
        recommendation: 'Another recommendation from same paper',
        topic: 'attention',
        status: 'standard',
        source: {
          paper: 'Dao et al. (2022)',
          year: 2022
        }
      }
    };

    render(
      <RecommendationCard
        recommendation={mockRecommendation}
        allRecommendations={multipleRecsFromSamePaper}
        onExpand={mockOnExpand}
      />
    );

    expect(screen.getByText('Other recommendations from this paper')).toBeInTheDocument();
    expect(screen.getByText('Another recommendation from same paper')).toBeInTheDocument();
  });

  it('calls onExpand when expand button is clicked', () => {
    render(
      <RecommendationCard
        recommendation={mockRecommendation}
        allRecommendations={mockAllRecommendations}
        onExpand={mockOnExpand}
      />
    );

    const expandButton = screen.getByRole('button');
    fireEvent.click(expandButton);

    expect(mockOnExpand).toHaveBeenCalledWith('MLR-2022-001');
  });

  it('handles recommendation with no related items', () => {
    const singleRecommendation = {
      id: 'MLR-2022-003',
      recommendation: 'Standalone recommendation',
      topic: 'unique-topic',
      status: 'standard',
      source: {
        paper: 'Unique Paper (2022)',
        year: 2022
      }
    };

    render(
      <RecommendationCard
        recommendation={singleRecommendation}
        allRecommendations={{ 'MLR-2022-003': singleRecommendation }}
        onExpand={mockOnExpand}
      />
    );

    // RelatedRecommendations should not render anything when there are no related items
    expect(screen.queryByText('Other recommendations from this paper')).not.toBeInTheDocument();
    expect(screen.queryByText('Related recommendations in this topic')).not.toBeInTheDocument();
  });

  it('handles missing arxiv_id gracefully', () => {
    const recWithoutArxiv = {
      ...mockRecommendation,
      source: {
        paper: 'Paper without arXiv (2022)',
        year: 2022
      }
    };

    render(
      <RecommendationCard
        recommendation={recWithoutArxiv}
        allRecommendations={mockAllRecommendations}
        onExpand={mockOnExpand}
      />
    );

    // Should not render arxiv link
    expect(screen.queryByRole('link')).not.toBeInTheDocument();
    // But should still render paper reference
    expect(screen.getByText('Paper without arXiv (2022)')).toBeInTheDocument();
  });
});
