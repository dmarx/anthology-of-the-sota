// src/components/recommendations/RecommendationCard/RecommendationInfo.tsx
export const RecommendationInfo: React.FC<RecommendationInfoProps> = ({ recommendation }) => (
  <>
    <div className="flex justify-between items-start mb-2">
      <div className="text-sm text-gray-500" data-testid="recommendation-id">
        {recommendation.id}
      </div>
    </div>
    <p className="font-medium mb-3" data-testid="recommendation-text">
      {recommendation.recommendation}
    </p>
    <div className="flex flex-wrap gap-2 mb-3">
      <span 
        className="px-2 py-1 text-sm rounded bg-green-100 text-green-800"
        data-testid="recommendation-status"
      >
        {recommendation.status}
      </span>
      <span 
        className="px-2 py-1 bg-blue-50 text-blue-700 rounded text-sm"
        data-testid="recommendation-topic"
      >
        {recommendation.topic}
      </span>
    </div>
  </>
);
