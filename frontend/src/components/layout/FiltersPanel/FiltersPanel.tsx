// frontend/src/components/layout/FiltersPanel/FiltersPanel.tsx
import React from 'react';
import { X } from 'lucide-react';
import { StatusFilter } from './StatusFilter';

interface FiltersPanelProps {
  isOpen: boolean;
  onClose: () => void;
  activeStatus: string[];
  onStatusChange: (status: string) => void;
}

export const FiltersPanel: React.FC<FiltersPanelProps> = ({
  isOpen,
  onClose,
  activeStatus,
  onStatusChange
}) => (
  <>
    {isOpen && (
      <div 
        className="fixed inset-0 bg-black/20 z-50"
        onClick={onClose}
      />
    )}
    
    <div className={`
      fixed right-0 top-0 h-full w-80 bg-white border-l shadow-lg z-50
      transform transition-transform duration-200
      ${isOpen ? 'translate-x-0' : 'translate-x-full'}
    `}>
      <div className="p-4 border-b flex items-center justify-between">
        <h2 className="font-semibold text-gray-900">Filters</h2>
        <button onClick={onClose} className="hover:bg-gray-100 p-1 rounded">
          <X size={20} />
        </button>
      </div>
      
      <StatusFilter
        activeStatus={activeStatus}
        onStatusChange={onStatusChange}
      />
      
      <div className="p-4 border-t mt-auto">
        <button
          onClick={onClose}
          className="w-full py-2 px-4 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          Apply Filters
        </button>
      </div>
    </div>
  </>
);
