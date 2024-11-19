
// frontend/src/pages/index.tsx
import React from 'react'
import { RecommendationCard } from '@/components/recommendations/RecommendationCard/RecommendationCard'
import type { Recommendation } from '@/types/recommendations'

interface HomeProps {
  recommendations: Record<string, Recommendation>;
}

export default function Home({ recommendations }: HomeProps) {
  const [expandedId, setExpandedId] = React.useState<string | null>(null);
  
  return (
    <main className="min-h-screen p-4">
      <div className="max-w-7xl mx-auto grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
        {Object.values(recommendations).map(rec => (
          <RecommendationCard
            key={rec.id}
            recommendation={rec}
            allRecommendations={recommendations}
            onExpand={setExpandedId}
          />
        ))}
      </div>
    </main>
  )
}

export async function getStaticProps() {
  // In a static site, we can import the data directly
  const recommendations = require('../../../data/registry.yaml');
  return {
    props: {
      recommendations: recommendations.recommendations.standard
    }
  }
}
