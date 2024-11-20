// src/components/recommendations/RecommendationCard/__tests__/RecommendationInfo.test.tsx
import { render, screen } from '@testing-library/react';
import { RecommendationInfo } from '../RecommendationInfo';

describe('RecommendationInfo', () => {
  const mockRecommendation = {
    id: 'MLR-2022-001',
    recommendation: 'Test recommendation',
    topic: 'testing',
    status: 'standard',
    source: {
      paper: 'Test Paper',
      year: 2022,
      first_author: 'Test'
    }
  };

  it('renders recommendation details correctly', () => {
    render(<RecommendationInfo recommendation={mockRecommendation} />);

    expect(screen.getByTestId('recommendation-id')).toHaveTextContent('MLR-2022-001');
    expect(screen.getByTestId('recommendation-text')).toHaveTextContent('Test recommendation');
    expect(screen.getByText('testing')).toBeInTheDocument();
    expect(screen.getByText('standard')).toBeInTheDocument();
  });
});
