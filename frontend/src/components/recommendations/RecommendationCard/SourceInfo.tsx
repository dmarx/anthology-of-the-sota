// src/components/recommendations/RecommendationCard/SourceInfo.tsx
import React from 'react';
import { ArxivLink } from '../ArxivLink/ArxivLink';
import type { Source } from '@/types/recommendations';

interface SourceInfoProps {
  source: Source;
}

export const SourceInfo: React.FC<SourceInfoProps> = ({ source }) => (
  <div className="text-sm text-gray-600">
    <p className="mb-1">{source.paper}</p>
    {source.arxiv_id && <ArxivLink arxivId={source.arxiv_id} />}
  </div>
);
