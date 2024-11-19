// frontend/src/utils/recommendations.ts
import type { Recommendation } from '@/types/recommendations';

export function getRecommendationChain(
  recommendation: Recommendation,
  allRecommendations: Record<string, Recommendation>
): Recommendation[] {
  const chain = [recommendation];
  let current = recommendation;
  
  while (current.superseded_by && allRecommendations[current.superseded_by]) {
    current = allRecommendations[current.superseded_by];
    chain.push(current);
  }
  
  return chain;
}

export function getRelatedRecommendations(
  recommendation: Recommendation,
  allRecommendations: Record<string, Recommendation>
): Recommendation[] {
  return Object.values(allRecommendations).filter(rec => 
    rec.id !== recommendation.id && (
      rec.source.paper === recommendation.source.paper ||
      rec.topic === recommendation.topic
    )
  );
}

// frontend/src/utils/recommendations.ts
export function groupRecommendationsByTopic(
  recommendations: Recommendation[]
): Record<string, Recommendation[]> {
  return recommendations.reduce((acc, rec) => {
    if (!acc[rec.topic]) {
      acc[rec.topic] = [];
    }
    acc[rec.topic].push(rec);
    return acc;
  }, {} as Record<string, Recommendation[]>);
}
