// frontend/src/pages/__tests__/index.test.tsx
import { render, screen } from '@testing-library/react';
import Home from '../index';

const mockRecommendations = [
  {
    id: 'MLR-2023-001',
    recommendation: 'Test recommendation',
    topic: 'testing',
    status: 'standard',
    source: {
      paper: 'Test Paper',
      year: 2023,
      first_author: 'Test Author'
    }
  }
];

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
