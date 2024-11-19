// src/components/recommendations/SuccessionChain/SuccessionChain.test.tsx
import { render, screen } from '@testing-library/react';
import { SuccessionChain } from './SuccessionChain';

const mockRecommendations = {
  'MLR-2020-001': {
    id: 'MLR-2020-001',
    source: { year: 2020 },
    superseded_by: 'MLR-2021-001'
  },
  'MLR-2021-001': {
    id: 'MLR-2021-001',
    source: { year: 2021 },
    superseded_by: 'MLR-2022-001'
  },
  'MLR-2022-001': {
    id: 'MLR-2022-001',
    source: { year: 2022 }
  }
};

describe('SuccessionChain', () => {
  it('renders complete chain of recommendations', () => {
    render(
      <SuccessionChain
        recommendations={mockRecommendations}
        currentId="MLR-2020-001"
      />
    );
    
    expect(screen.getByText('MLR-2020-001')).toBeInTheDocument();
    expect(screen.getByText('MLR-2021-001')).toBeInTheDocument();
    expect(screen.getByText('MLR-2022-001')).toBeInTheDocument();
  });

  it('highlights current recommendation', () => {
    render(
      <SuccessionChain
        recommendations={mockRecommendations}
        currentId="MLR-2021-001"
      />
    );
    
    const currentElement = screen.getByText('MLR-2021-001').closest('div');
    expect(currentElement).toHaveClass('bg-blue-100');
  });
});
