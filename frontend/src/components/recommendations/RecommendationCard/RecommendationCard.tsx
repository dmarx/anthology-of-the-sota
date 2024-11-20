// src/components/recommendations/RecommendationCard/RecommendationCard.tsx
import React from 'react';
import { Tag } from 'lucide-react';
import { RecommendationInfo } from './RecommendationInfo';
import { SourceInfo } from './SourceInfo';
import { SupersessionInfo } from './SupersessionInfo';
import { SuccessionChain } from '../SuccessionChain/SuccessionChain';
import { RelatedRecommendations } from '../RelatedRecommendations/RelatedRecommendations';
import type { Recommendation } from '@/types/recommendations';

interface RecommendationCardProps {
  recommendation: Recommendation;
  allRecommendations: Record<string, Recommendation>;
  onExpand: (id: string) => void;
}

export const RecommendationCard: React.FC<RecommendationCardProps> = ({
  recommendation,
  allRecommendations,
  onExpand
}) => (
  <div className="p-4 border rounded-lg shadow-sm bg-white hover:shadow-md transition-shadow">
    <RecommendationInfo recommendation={recommendation} />
    <SourceInfo source={recommendation.source} />

    {recommendation.superseded_by && allRecommendations[recommendation.superseded_by] && (
      <>
        <SupersessionInfo 
          recommendation={recommendation}
          supersededBy={allRecommendations[recommendation.superseded_by]} 
        />
        <SuccessionChain
          recommendations={allRecommendations}
          currentId={recommendation.id}
        />
      </>
    )}

    <RelatedRecommendations 
      paper={recommendation.source.paper}
      recommendations={allRecommendations}
    />
  </div>
);
