// src/components/recommendations/SuccessionChain/SuccessionChain.tsx
import React from 'react';
import { GitBranch } from 'lucide-react';
import { Recommendation } from '@/types/recommendations';

interface SuccessionChainProps {
  recommendations: Record<string, Recommendation>;
  currentId: string;
}

export const SuccessionChain: React.FC<SuccessionChainProps> = ({ recommendations, currentId }) => {
  const findChain = (id: string, chain: Recommendation[] = []): Recommendation[] => {
    const rec = recommendations[id];
    if (!rec) return chain;
    
    if (rec.superseded_by) {
      return findChain(rec.superseded_by, [...chain, rec]);
    }
    return [...chain, rec];
  };

  const chain = findChain(currentId);
  
  return (
    <div className="flex flex-col gap-2 mt-4">
      <h4 className="text-sm font-medium text-gray-700">Recommendation Evolution</h4>
      <div className="flex items-center gap-2 overflow-x-auto">
        {chain.map((rec, idx) => (
          <React.Fragment key={rec.id}>
            <div className={`p-2 rounded ${rec.id === currentId ? 'bg-blue-100 border-blue-300' : 'bg-gray-50 border-gray-200'} border`}>
              <div className="text-sm font-medium">{rec.id}</div>
              <div className="text-xs text-gray-600">{rec.source.year}</div>
            </div>
            {idx < chain.length - 1 && <GitBranch className="text-gray-400" size={16} />}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};
