// frontend/src/components/layout/Layout.tsx
import React, { useState } from 'react';
import { Menu } from 'lucide-react';
import { Header } from './Header/Header';
import { Sidebar } from './Sidebar/Sidebar';
import { FiltersPanel } from './FiltersPanel/FiltersPanel';
import { ActiveFilters } from '../recommendations/ActiveFilters/ActiveFilters';
import { useSearch } from '../../contexts/search/SearchContext';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [filtersOpen, setFiltersOpen] = useState(false);
  
  const { state, dispatch } = useSearch();
  
  // Example topics - in practice, these would be derived from your data
  const topics = [
    'attention',
    'optimization',
    'training-dynamics',
    'distributed-training',
    'memory-efficiency',
    'hardware-optimization'
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Header 
        onSearch={(query) => dispatch({ type: 'SET_SEARCH', query })}
        openFilters={() => setFiltersOpen(true)}
      />
      
      <div className="flex">
        <Sidebar
          topics={topics}
          activeTopics={state.topics}
          onTopicChange={(topic) => dispatch({ type: 'TOGGLE_TOPIC', topic })}
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
        />
        
        <main className="flex-1 p-4">
          <div className="max-w-7xl mx-auto">
            {/* Mobile menu button */}
            <button
              onClick={() => setSidebarOpen(true)}
              className="md:hidden mb-4 p-2 hover:bg-gray-100 rounded"
            >
              <Menu size={24} />
            </button>
            
            <ActiveFilters
              topics={state.topics}
              searchQuery={state.searchQuery}
              onRemoveTopic={(topic) => dispatch({ type: 'TOGGLE_TOPIC', topic })}
              onClearSearch={() => dispatch({ type: 'SET_SEARCH', query: '' })}
            />
            
            {children}
          </div>
        </main>
      </div>

      <FiltersPanel
        isOpen={filtersOpen}
        onClose={() => setFiltersOpen(false)}
        activeStatus={state.status}
        onStatusChange={(status) => dispatch({ type: 'TOGGLE_STATUS', status })}
      />
    </div>
  );
};
