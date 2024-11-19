// frontend/src/components/recommendations/RecommendationCard/RecommendationCard.tsx
import React from 'react';
import { Tag } from 'lucide-react';
import { ArxivLink } from '../ArxivLink/ArxivLink';
import type { Recommendation } from '../../../types/recommendations';

interface RecommendationCardProps {
  recommendation: Recommendation;
  allRecommendations: Record<string, Recommendation>;
  onExpand: (id: string) => void;
}

export const RecommendationCard: React.FC<RecommendationCardProps> = ({
  recommendation,
  allRecommendations,
  onExpand
}) => {
  const statusColors = {
    standard: 'bg-green-100 text-green-800',
    experimental: 'bg-yellow-100 text-yellow-800',
    deprecated: 'bg-red-100 text-red-800'
  };

  // Safely access implementations with default empty array
  const implementations = recommendation.implementations || [];

  return (
    <div className="p-4 border rounded-lg shadow-sm bg-white hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-2">
        <div className="text-sm text-gray-500">{recommendation.id}</div>
        <button 
          onClick={() => onExpand(recommendation.id)}
          className="text-blue-500 hover:text-blue-600"
        >
          <Tag size={16} />
        </button>
      </div>
      
      <p className="font-medium mb-3">{recommendation.recommendation}</p>
      
      <div className="flex flex-wrap gap-2 mb-3">
        <span className={`px-2 py-1 text-sm rounded ${statusColors[recommendation.status]}`}>
          {recommendation.status}
        </span>
      </div>
      
      <div className="text-sm text-gray-600">
        <p className="mb-1">{recommendation.source.paper}</p>
        {recommendation.source.arxiv_id && (
          <ArxivLink arxivId={recommendation.source.arxiv_id} />
        )}
      </div>

      {implementations.length > 0 && (
        <div className="mt-2 text-sm">
          <span className="text-gray-500">Implementations: </span>
          <span>{implementations.join(', ')}</span>
        </div>
      )}

      {recommendation.superseded_by && (
        <div className="mt-2 text-sm text-red-600">
          Superseded by: {allRecommendations[recommendation.superseded_by]?.recommendation || recommendation.superseded_by}
        </div>
      )}
    </div>
  );
}
