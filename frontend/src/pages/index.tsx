// frontend/src/pages/index.tsx
import React from 'react';
import { parse } from 'yaml';
import { RecommendationCard } from '../components/recommendations/RecommendationCard/RecommendationCard';
import { groupRecommendationsByTopic } from '../utils/recommendations';
import type { Recommendation } from '../types/recommendations';

interface HomeProps {
  recommendations: Recommendation[];
  error?: string;
}

export default function Home({ recommendations, error }: HomeProps) {
  if (error) {
    return (
      <div className="min-h-screen p-4 bg-gray-50">
        <div className="max-w-7xl mx-auto p-4 bg-red-50 border border-red-200 rounded">
          <h1 className="text-red-800 text-xl font-bold">Error Loading Data</h1>
          <p className="text-red-600">{error}</p>
        </div>
      </div>
    );
  }

  if (!recommendations || recommendations.length === 0) {
    return (
      <div className="min-h-screen p-4 bg-gray-50">
        <div className="max-w-7xl mx-auto p-4 bg-gray-100 border border-gray-200 rounded">
          <h1 className="text-gray-800 text-xl font-bold">No Recommendations</h1>
          <p className="text-gray-600">No recommendations are currently available.</p>
        </div>
      </div>
    );
  }

  // Group recommendations by topic
  const recommendationsByTopic = groupRecommendationsByTopic(recommendations);
  
  // Create lookup table for all recommendations
  const recommendationsMap = recommendations.reduce((acc, rec) => {
    acc[rec.id] = rec;
    return acc;
  }, {} as Record<string, Recommendation>);

  return (
    <div className="min-h-screen bg-gray-50">
      <main className="max-w-7xl mx-auto p-4">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">
          ML Training Recommendations
        </h1>
        
        {Object.entries(recommendationsByTopic)
          .sort(([a], [b]) => a.localeCompare(b))
          .map(([topic, recs]) => (
            <section key={topic} className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4 capitalize">
                {topic.replace(/-/g, ' ')}
              </h2>
              <div className="grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
                {recs.map((rec) => (
                  <RecommendationCard
                    key={rec.id}
                    recommendation={rec}
                    allRecommendations={recommendationsMap}
                    onExpand={() => {}}
                  />
                ))}
              </div>
            </section>
        ))}
      </main>
    </div>
  );
}

export async function getStaticProps() {
  try {
    const fs = require('fs');
    const path = require('path');
    const yamlPath = path.join(process.cwd(), 'src/data/registry.yaml');
    
    console.log('Loading YAML from:', yamlPath);
    const yamlContent = fs.readFileSync(yamlPath, 'utf8');
    const data = parse(yamlContent);
    
    // Validate data structure
    if (!data?.recommendations || !Array.isArray(data.recommendations)) {
      throw new Error('Invalid data structure: recommendations should be an array');
    }

    return {
      props: {
        recommendations: data.recommendations
      }
    };
  } catch (error: any) {
    console.error('Error in getStaticProps:', error);
    return {
      props: {
        recommendations: [],
        error: error.message
      }
    };
  }
}
