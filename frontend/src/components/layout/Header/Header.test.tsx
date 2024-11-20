// frontend/src/components/layout/Header/Header.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Header } from './Header';

describe('Header', () => {
  const mockOnSearch = jest.fn();
  const mockOpenFilters = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders title and search bar', () => {
    render(<Header onSearch={mockOnSearch} openFilters={mockOpenFilters} />);
    
    expect(screen.getByText('ML Training Recommendations')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Search recommendations...')).toBeInTheDocument();
  });

  it('calls onSearch when search input changes', () => {
    render(<Header onSearch={mockOnSearch} openFilters={mockOpenFilters} />);
    
    const searchInput = screen.getByPlaceholderText('Search recommendations...');
    fireEvent.change(searchInput, { target: { value: 'test' } });
    
    expect(mockOnSearch).toHaveBeenCalledWith('test');
  });

  it('calls openFilters when filter button is clicked', () => {
    render(<Header onSearch={mockOnSearch} openFilters={mockOpenFilters} />);
    
    const filterButton = screen.getByText('Filters');
    fireEvent.click(filterButton);
    
    expect(mockOpenFilters).toHaveBeenCalled();
  });
});
