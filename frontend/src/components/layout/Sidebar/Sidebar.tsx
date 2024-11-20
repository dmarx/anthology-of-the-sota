// frontend/src/components/layout/Sidebar/Sidebar.tsx
import React from 'react';
import { X } from 'lucide-react';
import { TopicList } from './TopicList';

interface SidebarProps {
  topics: string[];
  activeTopics: string[];
  onTopicChange: (topic: string) => void;
  isOpen: boolean;
  onClose: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
  topics,
  activeTopics,
  onTopicChange,
  isOpen,
  onClose
}) => (
  <>
    {/* Mobile backdrop */}
    {isOpen && (
      <div 
        className="fixed inset-0 bg-black/20 z-40 md:hidden"
        onClick={onClose}
      />
    )}
    
    <aside className={`
      fixed top-0 left-0 h-full w-64 bg-white border-r shadow-lg z-50 transform transition-transform
      ${isOpen ? 'translate-x-0' : '-translate-x-full'}
      md:translate-x-0 md:static md:z-0
    `}>
      <div className="p-4 border-b flex items-center justify-between md:justify-center">
        <h2 className="font-semibold text-gray-900">Topics</h2>
        <button onClick={onClose} className="md:hidden">
          <X size={20} />
        </button>
      </div>
      
      <TopicList 
        topics={topics}
        activeTopics={activeTopics}
        onTopicChange={onTopicChange}
      />
    </aside>
  </>
);
