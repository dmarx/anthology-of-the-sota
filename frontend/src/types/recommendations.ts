// frontend/src/types/recommendations.ts
// export type RecommendationStatus = 'standard' | 'experimental' | 'deprecated';

export interface Source {
  paper: string
  paper_id: string
  year: number
  first_author: string
  arxiv_id?: string
}

export interface Recommendation {
  id: string
  recommendation: string
  topic: string
  topic_id: string
  source: Source
  status: 'standard' | 'experimental' | 'deprecated'
  supporting_evidence: any[]
  implementations: string[]
}

export type RecommendationsByTopic = Record<string, Recommendation[]>
