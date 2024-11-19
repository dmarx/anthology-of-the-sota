// src/components/recommendations/ArxivLink/ArxivLink.test.tsx
import { render, screen } from '@testing-library/react';
import { ArxivLink } from './ArxivLink';

describe('ArxivLink', () => {
  it('renders arxiv link with correct ID', () => {
    render(<ArxivLink arxivId="2205.14135" />);
    
    const link = screen.getByRole('link');
    expect(link).toHaveAttribute('href', 'https://arxiv.org/abs/2205.14135');
    expect(link).toHaveAttribute('target', '_blank');
    expect(link).toHaveAttribute('rel', 'noopener noreferrer');
    expect(screen.getByText('arXiv:2205.14135')).toBeInTheDocument();
  });
});
