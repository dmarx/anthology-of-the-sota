// frontend/src/components/recommendations/SuccessionChain/SuccessionChain.tsx
import React from 'react';
import { GitBranch } from 'lucide-react';
import type { Recommendation } from '@/types/recommendations';

interface SuccessionChainProps {
  recommendations: Record<string, Recommendation>;
  currentId: string;
}

export const SuccessionChain: React.FC<SuccessionChainProps> = ({ recommendations, currentId }) => {
  const findChain = (id: string): Recommendation[] => {
    const rec = recommendations[id];
    if (!rec) return [];
    
    if (rec.superseded_by) {
      return [rec, ...findChain(rec.superseded_by)];
    }
    return [rec];
  };

  const chain = findChain(currentId);
  
  if (chain.length <= 1) return null;
  
  return (
    <div className="mt-4">
      <h4 className="text-sm font-medium text-gray-700">Recommendation Evolution</h4>
      <div className="flex items-center gap-2 mt-2 overflow-x-auto">
        {chain.map((rec, idx) => (
          <React.Fragment key={rec.id}>
            <div 
              className={`p-2 rounded ${rec.id === currentId ? 'bg-blue-100' : 'bg-gray-50'}`}
            >
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
