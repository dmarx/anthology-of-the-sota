// src/components/recommendations/RecommendationCard/SupersessionInfo.tsx
import React from 'react';
import type { Recommendation } from '@/types/recommendations';

interface SupersessionInfoProps {
  recommendation: Recommendation;
  supersededBy: Recommendation;
}

export const SupersessionInfo: React.FC<SupersessionInfoProps> = ({
  recommendation,
  supersededBy
}) => (
  <div className="mt-2 text-sm text-red-600">
    Superseded by: {supersededBy?.recommendation || recommendation.superseded_by}
  </div>
);
