// frontend/src/pages/index.tsx
import React from 'react';
import { Layout } from '@/components/layout/Layout';
import { RecommendationGrid } from '@/components/recommendations/RecommendationGrid/RecommendationGrid';
import { SearchProvider, useSearch } from '@/contexts/search/SearchContext';
import type { Recommendation } from '@/types/recommendations';

interface HomeContentProps {
  recommendations: Recommendation[];
}

const HomeContent: React.FC<HomeContentProps> = ({ recommendations }) => {
  const { 
    state,
    filterRecommendations, 
    sortRecommendations 
  } = useSearch();

  const filteredRecs = sortRecommendations(filterRecommendations(recommendations));

  return (
    <RecommendationGrid
      recommendations={filteredRecs}
      view={state.view}
      onExpand={() => {}}
    />
  );
};

export default function Home({ recommendations = [] }: { recommendations?: Recommendation[] }) {
  return (
    <SearchProvider>
      <Layout>
        <HomeContent recommendations={recommendations} />
      </Layout>
    </SearchProvider>
  );
}

export async function getStaticProps() {
  try {
    const fs = require('fs');
    const path = require('path');
    const { parse } = require('yaml');
    
    const yamlPath = path.join(process.cwd(), 'src/data/registry.yaml');
    console.log('Loading YAML from:', yamlPath);
    
    if (!fs.existsSync(yamlPath)) {
      console.warn('Registry file not found, returning empty array');
      return { props: { recommendations: [] } };
    }
    
    const yamlContent = fs.readFileSync(yamlPath, 'utf8');
    const data = parse(yamlContent);
    
    if (!data?.recommendations) {
      console.warn('No recommendations found in registry');
      return { props: { recommendations: [] } };
    }

    // Fixed type error by adding explicit type casting and safety checks
    const recommendations = Object.entries(data.recommendations.standard || {})
      .reduce<Recommendation[]>((acc, [topic, recs]) => {
        if (typeof recs === 'object' && recs !== null) {
          return [...acc, ...Object.values(recs as Record<string, Recommendation>)];
        }
        return acc;
      }, []);

    return {
      props: {
        recommendations
      }
    };
  } catch (error: any) {
    console.error('Error in getStaticProps:', error);
    return { props: { recommendations: [] } };
  }
}
