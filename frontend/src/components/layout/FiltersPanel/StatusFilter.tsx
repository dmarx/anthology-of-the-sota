// frontend/src/components/layout/FiltersPanel/StatusFilter.tsx
import React from 'react';

interface StatusFilterProps {
  activeStatus: string[];
  onStatusChange: (status: string) => void;
}

export const StatusFilter: React.FC<StatusFilterProps> = ({ 
  activeStatus, 
  onStatusChange 
}) => {
  const statuses = ['standard', 'experimental', 'deprecated'];
  
  return (
    <div className="p-4">
      <h3 className="font-medium text-gray-900 mb-3">Status</h3>
      <div className="space-y-2">
        {statuses.map(status => (
          <label key={status} className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={activeStatus.includes(status)}
              onChange={() => onStatusChange(status)}
              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
            />
            <span className="text-sm text-gray-700 capitalize">{status}</span>
          </label>
        ))}
      </div>
    </div>
  );
};
