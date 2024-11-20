// frontend/src/pages/index.tsx
import React from 'react';
import { Layout } from '../components/layout/Layout';
import { RecommendationGrid } from '../components/recommendations/RecommendationGrid/RecommendationGrid';
import { SearchProvider, useSearch } from '../contexts/search/SearchContext';
import type { Recommendation } from '../types/recommendations';

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

// Add default value to getStaticProps
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

    return {
      props: {
        recommendations: Object.values(data.recommendations)
          .flatMap(topicRecs => Object.values(topicRecs))
          .flat()
      }
    };
  } catch (error: any) {
    console.error('Error in getStaticProps:', error);
    // Return empty array instead of error in production
    return {
      props: {
        recommendations: []
      }
    };
  }
}
