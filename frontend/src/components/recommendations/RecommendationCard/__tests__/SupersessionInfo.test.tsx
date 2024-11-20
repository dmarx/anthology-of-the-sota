// src/components/recommendations/RecommendationCard/__tests__/SupersessionInfo.test.tsx
import { render, screen } from '@testing-library/react';
import { SupersessionInfo } from '../SupersessionInfo';

describe('SupersessionInfo', () => {
  const mockRecommendation = {
    id: 'MLR-2022-001',
    recommendation: 'Old recommendation',
    superseded_by: 'MLR-2023-001'
  };

  const mockSupersededBy = {
    id: 'MLR-2023-001',
    recommendation: 'New recommendation'
  };

  it('shows supersession information', () => {
    render(
      <SupersessionInfo 
        recommendation={mockRecommendation} 
        supersededBy={mockSupersededBy} 
      />
    );

    expect(screen.getByText(/Superseded by:/)).toBeInTheDocument();
    expect(screen.getByText(/New recommendation/)).toBeInTheDocument();
  });
});
