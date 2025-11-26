// src/app/models/candidate.model.ts
export interface CandidateSummary {
  user_id: number;
  full_name: string;
  email: string;
  department: string;
  country: string;
  latest_cv_title: string;
  skills: string;
  availability: number;
  clearance?: string;
}
