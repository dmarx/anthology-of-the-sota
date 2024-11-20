// frontend/src/components/recommendations/RecommendationGrid/RecommendationGrid.tsx
import React from 'react';
import { RecommendationCard } from '../RecommendationCard/RecommendationCard';
import type { Recommendation } from '../../../types/recommendations';

interface RecommendationGridProps {
  recommendations: Recommendation[];
  view: 'grid' | 'list';
  onExpand: (id: string) => void;
}

export const RecommendationGrid: React.FC<RecommendationGridProps> = ({
  recommendations,
  view,
  onExpand
}) => {
  if (recommendations.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500 text-lg">
          No recommendations match your current filters.
        </p>
      </div>
    );
  }

  return (
    <div className={
      view === 'grid'
        ? "grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3"
        : "space-y-4"
    }>
      {recommendations.map(rec => (
        <RecommendationCard
          key={rec.id}
          recommendation={rec}
          allRecommendations={recommendations.reduce((acc, r) => ({
            ...acc,
            [r.id]: r
          }), {})}
          onExpand={onExpand}
        />
      ))}
    </div>
  );
};
