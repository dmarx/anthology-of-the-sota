// src/components/recommendations/RecommendationCard/__tests__/SourceInfo.test.tsx
import { render, screen } from '@testing-library/react';
import { SourceInfo } from '../SourceInfo';

describe('SourceInfo', () => {
  const mockSource = {
    paper: 'Test Paper',
    year: 2022,
    first_author: 'Test',
    arxiv_id: '2205.14135'
  };

  it('renders source information', () => {
    render(<SourceInfo source={mockSource} />);

    expect(screen.getByText('Test Paper')).toBeInTheDocument();
    expect(screen.getByText('arXiv:2205.14135')).toBeInTheDocument();
  });

  it('handles missing arxiv id', () => {
    const sourceWithoutArxiv = { ...mockSource, arxiv_id: undefined };
    render(<SourceInfo source={sourceWithoutArxiv} />);

    expect(screen.getByText('Test Paper')).toBeInTheDocument();
    expect(screen.queryByText(/arXiv:/)).not.toBeInTheDocument();
  });
});
