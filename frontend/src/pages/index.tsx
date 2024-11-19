import React from 'react';
import { parse } from 'yaml';
import { RecommendationCard } from '../components/recommendations/RecommendationCard/RecommendationCard';
import type { Recommendation } from '../types/recommendations';

interface HomeProps {
  recommendations: Record<string, Recommendation>;
  error?: string;
}

export default function Home({ recommendations, error }: HomeProps) {
  if (error) {
    return (
      <div className="min-h-screen p-4">
        <div className="max-w-7xl mx-auto p-4 bg-red-50 border border-red-200 rounded">
          <h1 className="text-red-800 text-xl font-bold">Error Loading Data</h1>
          <p className="text-red-600">{error}</p>
        </div>
      </div>
    );
  }

  if (!recommendations || Object.keys(recommendations).length === 0) {
    return (
      <div className="min-h-screen p-4">
        <div className="max-w-7xl mx-auto p-4 bg-gray-50 border border-gray-200 rounded">
          <h1 className="text-gray-800 text-xl font-bold">No Recommendations</h1>
          <p className="text-gray-600">No recommendations are currently available.</p>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen p-4">
      <div className="max-w-7xl mx-auto grid gap-4 grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
        {Object.entries(recommendations).map(([id, rec]) => (
          <RecommendationCard
            key={id}
            recommendation={rec}
            allRecommendations={recommendations}
            onExpand={() => {}}
          />
        ))}
      </div>
    </main>
  );
}

export async function getStaticProps() {
  try {
    const fs = require('fs');
    const path = require('path');
    
    console.log('Current directory:', process.cwd());
    console.log('Files in data directory:', fs.readdirSync(path.join(process.cwd(), 'src/data')));
    
    const yamlPath = path.join(process.cwd(), 'src/data/registry.yaml');
    console.log('Loading YAML from:', yamlPath);
    
    const yamlContent = fs.readFileSync(yamlPath, 'utf8');
    console.log('YAML content length:', yamlContent.length);
    
    const data = parse(yamlContent);
    console.log('Parsed data structure:', Object.keys(data));
    
    if (!data || !data.recommendations || !data.recommendations.standard) {
      throw new Error('Invalid data structure in registry.yaml');
    }
    
    console.log('Number of recommendations:', Object.keys(data.recommendations.standard).length);
    return {
      props: {
        recommendations: data.recommendations.standard
      }
    };
  } catch (error: unknown) {
    console.error('Error in getStaticProps:', error);
    
    if (process.env.NODE_ENV === 'development') {
      return {
        props: {
          recommendations: {},
          error: error instanceof Error ? error.message : 'An unknown error occurred'
        }
      };
    }
    
    return {
      props: {
        recommendations: {}
      }
    };
  }
}
