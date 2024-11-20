// src/pages/__tests__/index.test.tsx
describe('Home Page', () => {
  it('renders with recommendations', () => {
    render(<Home recommendations={mockRecommendations} />);
    
    // Use testid instead of text content
    expect(screen.getByTestId('recommendation-text')).toHaveTextContent('Test recommendation');
  });
});
