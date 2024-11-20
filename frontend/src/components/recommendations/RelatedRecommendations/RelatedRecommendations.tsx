// src/components/recommendations/RelatedRecommendations/RelatedRecommendations.tsx
export const RelatedRecommendations: React.FC<RelatedRecommendationsProps> = ({ 
  paper, 
  recommendations 
}) => {
  const related = useMemo(() => {
    return Object.values(recommendations).filter(rec => 
      paper && rec.source.paper === paper
    );
  }, [paper, recommendations]);

  if (!related.length) return null;

  return (
    <div className="mt-4" data-testid="related-recommendations">
      <h4 className="text-sm font-medium text-gray-700">
        Other recommendations from this paper
      </h4>
      <div className="mt-2 space-y-2">
        {related.map(rec => (
          <div key={rec.id} className="text-sm p-2 bg-gray-50 rounded">
            <div className="font-medium">{rec.recommendation}</div>
            <div className="text-xs text-gray-600 mt-1">{rec.id}</div>
          </div>
        ))}
      </div>
    </div>
  );
};
