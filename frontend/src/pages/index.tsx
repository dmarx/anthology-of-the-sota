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

export default function Home({ recommendations }: { recommendations: Recommendation[] }) {
  return (
    <SearchProvider>
      <Layout>
        <HomeContent recommendations={recommendations} />
      </Layout>
    </SearchProvider>
  );
}
