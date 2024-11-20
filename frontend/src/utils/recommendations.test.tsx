
// src/utils/recommendations.test.tsx
import { 
  getRecommendationChain, 
  getRelatedRecommendations,
  groupRecommendationsByTopic 
} from './recommendations';
import type { Recommendation } from '@/types/recommendations';

describe('getRecommendationChain', () => {
  const mockRecommendations: Record<string, Recommendation> = {
    'MLR-2023-001': {
      id: 'MLR-2023-001',
      recommendation: 'Original',
      topic: 'test',
      topic_id: 'test/original',
      superseded_by: 'MLR-2023-002',
      source: {
        paper: 'Test Paper',
        paper_id: 'test123',
        year: 2023,
        first_author: 'Test'
      },
      status: 'deprecated'
    },
    'MLR-2023-002': {
      id: 'MLR-2023-002',
      recommendation: 'Updated',
      topic: 'test',
      topic_id: 'test/updated',
      source: {
        paper: 'Test Paper 2',
        paper_id: 'test456',
        year: 2023,
        first_author: 'Test'
      },
      status: 'standard'
    }
  };

  it('builds recommendation chain', () => {
    const chain = getRecommendationChain(
      mockRecommendations['MLR-2023-001'],
      mockRecommendations
    );
    
    expect(chain).toHaveLength(2);
    expect(chain[0].id).toBe('MLR-2023-001');
    expect(chain[1].id).toBe('MLR-2023-002');
  });
});

describe('getRelatedRecommendations', () => {
  const mockRecommendations: Record<string, Recommendation> = {
    'MLR-2023-001': {
      id: 'MLR-2023-001',
      recommendation: 'First',
      topic: 'test',
      topic_id: 'test/first',
      source: {
        paper: 'Test Paper',
        paper_id: 'test123',
        year: 2023,
        first_author: 'Test'
      },
      status: 'standard'
    },
    'MLR-2023-002': {
      id: 'MLR-2023-002',
      recommendation: 'Second',
      topic: 'test',
      topic_id: 'test/second',
      source: {
        paper: 'Test Paper',
        paper_id: 'test123',
        year: 2023,
        first_author: 'Test'
      },
      status: 'standard'
    }
  };

  it('finds related recommendations by paper', () => {
    const related = getRelatedRecommendations(
      mockRecommendations['MLR-2023-001'],
      mockRecommendations
    );
    
    expect(related).toHaveLength(1);
    expect(related[0].id).toBe('MLR-2023-002');
  });
});

describe('groupRecommendationsByTopic', () => {
  const mockRecommendations: Recommendation[] = [
    {
      id: 'MLR-2023-001',
      recommendation: 'First',
      topic: 'topic1',
      topic_id: 'topic1/first',
      source: {
        paper: 'Test Paper',
        paper_id: 'test123',
        year: 2023,
        first_author: 'Test'
      },
      status: 'standard'
    },
    {
      id: 'MLR-2023-002',
      recommendation: 'Second',
      topic: 'topic2',
      topic_id: 'topic2/second',
      source: {
        paper: 'Test Paper 2',
        paper_id: 'test456',
        year: 2023,
        first_author: 'Test'
      },
      status: 'standard'
    }
  ];

  it('groups recommendations by topic', () => {
    const grouped = groupRecommendationsByTopic(mockRecommendations);
    
    expect(Object.keys(grouped)).toHaveLength(2);
    expect(grouped.topic1).toHaveLength(1);
    expect(grouped.topic2).toHaveLength(1);
    expect(grouped.topic1[0].id).toBe('MLR-2023-001');
    expect(grouped.topic2[0].id).toBe('MLR-2023-002');
  });
});
