// frontend/src/components/recommendations/RecommendationCard/RecommendationCard.tsx
import React from 'react';
import { Tag } from 'lucide-react';
import { ArxivLink } from '../ArxivLink/ArxivLink';
import { SuccessionChain } from '../SuccessionChain/SuccessionChain';
import { RelatedRecommendations } from '../RelatedRecommendations/RelatedRecommendations';
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
  // Validate required data
  if (!recommendation || !recommendation.id || !recommendation.source) {
    console.error('Invalid recommendation data:', recommendation);
    return null;
  }

  return (
    <div className="p-4 border rounded-lg">
      <div className="flex justify-between items-start mb-2">
        <div className="text-sm text-gray-500">{recommendation.id}</div>
        <button onClick={() => onExpand(recommendation.id)}>
          <Tag size={16} className="text-blue-500" />
        </button>
      </div>
      
      <p className="font-medium mb-2">{recommendation.recommendation}</p>
      
      <div className="flex flex-wrap gap-2 mb-2">
        {recommendation.topic && (
          <span className="px-2 py-1 bg-blue-100 text-blue-800 text-sm rounded">
            {recommendation.topic}
          </span>
        )}
        {recommendation.status && (
          <span className="px-2 py-1 bg-green-100 text-green-800 text-sm rounded">
            {recommendation.status}
          </span>
        )}
      </div>
      
      <div className="text-sm text-gray-600">
        {recommendation.source.paper && (
          <p>{recommendation.source.paper}</p>
        )}
        {recommendation.source.arxiv_id && (
          <ArxivLink arxivId={recommendation.source.arxiv_id} />
        )}
      </div>

      {recommendation.superseded_by && (
        <SuccessionChain 
          recommendations={allRecommendations}
          currentId={recommendation.id}
        />
      )}

      <RelatedRecommendations 
        paper={recommendation.source.paper}
        topic={recommendation.topic}
        recommendations={allRecommendations}
      />
    </div>
  );
};
