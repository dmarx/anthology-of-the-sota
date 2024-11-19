// frontend/src/types/recommendations.ts
export type RecommendationStatus = 'standard' | 'experimental' | 'deprecated';

export interface Source {
  paper: string;
  paper_id: string;
  year: number;
  first_author: string;
  arxiv_id?: string;
}

export interface Recommendation {
  id: string;
  recommendation: string;
  topic: string;
  topic_id: string;
  source: Source;
  status: RecommendationStatus;
  supporting_evidence: any[];
  superseded_by?: string;
  deprecated_date?: string;
  implementations: string[];
}
