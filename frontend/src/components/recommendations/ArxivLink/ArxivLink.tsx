// src/components/recommendations/ArxivLink/ArxivLink.tsx
import React from 'react';
import { ExternalLink } from 'lucide-react';

interface ArxivLinkProps {
  arxivId: string;
}

export const ArxivLink: React.FC<ArxivLinkProps> = ({ arxivId }) => (
  <a 
    href={`https://arxiv.org/abs/${arxivId}`}
    target="_blank"
    rel="noopener noreferrer"
    className="inline-flex items-center gap-1 text-blue-600 hover:text-blue-800"
  >
    arXiv:{arxivId}
    <ExternalLink size={14} />
  </a>
);
