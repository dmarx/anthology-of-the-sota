// frontend/src/components/layout/Sidebar/TopicList.tsx
import React from 'react';

interface TopicListProps {
  topics: string[];
  activeTopics: string[];
  onTopicChange: (topic: string) => void;
}

export const TopicList: React.FC<TopicListProps> = ({ 
  topics, 
  activeTopics, 
  onTopicChange 
}) => (
  <nav className="p-4 space-y-2">
    {topics.map(topic => (
      <label 
        key={topic} 
        className="flex items-center gap-2 cursor-pointer p-2 hover:bg-gray-50 rounded"
      >
        <input
          type="checkbox"
          checked={activeTopics.includes(topic)}
          onChange={() => onTopicChange(topic)}
          className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
        />
        <span className="text-sm text-gray-700">{topic}</span>
      </label>
    ))}
  </nav>
);
