// src/components/recommendations/RelatedRecommendations/RelatedRecommendations.tsx
import React, { useMemo } from 'react';
import { Recommendation } from '@/types/recommendations';

interface RelatedRecommendationsProps {
  paper?: string;
  topic?: string;
  recommendations: Record<string, Recommendation>;
}

export const RelatedRecommendations: React.FC<RelatedRecommendationsProps> = ({ 
  paper, 
  topic, 
  recommendations 
}) => {
  const related = useMemo(() => {
    return Object.values(recommendations).filter(rec => 
      (paper && rec.source.paper === paper) || 
      (topic && rec.topic === topic)
    );
  }, [paper, topic, recommendations]);

  if (!related.length) return null;

  return (
    <div className="mt-4">
      <h4 className="text-sm font-medium text-gray-700">
        {paper ? 'Other recommendations from this paper' : 'Related recommendations in this topic'}
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
