// src/components/recommendations/SuccessionChain/SuccessionChain.tsx
export const SuccessionChain: React.FC<SuccessionChainProps> = ({ recommendations, currentId }) => (
  <div className="mt-4">
    <h4 className="text-sm font-medium text-gray-700">Recommendation Evolution</h4>
    <div className="flex items-center gap-2 mt-2 overflow-x-auto">
      {chain.map((rec, idx) => (
        <div key={rec.id}>
          <div
            data-testid={rec.id === currentId ? 'succession-current' : 'succession-next'}
            className={`p-2 rounded ${rec.id === currentId ? 'bg-blue-100' : 'bg-gray-50'}`}
          >
            <div className="text-sm font-medium">{rec.id}</div>
            <div className="text-xs text-gray-600">{rec.source.year}</div>
          </div>
          {idx < chain.length - 1 && <GitBranch className="text-gray-400" size={16} />}
        </div>
      ))}
    </div>
  </div>
);
