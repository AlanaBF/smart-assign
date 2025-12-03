// src/app/services/candidate.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CandidateSummary } from '../models/candidate.model';

@Injectable({
  providedIn: 'root'
})
export class CandidateService {
  private readonly baseUrl = 'http://localhost:8000/api';

  constructor(private readonly http: HttpClient) {}

  getAllCandidates(): Observable<CandidateSummary[]> {
    return this.http.get<CandidateSummary[]>(`${this.baseUrl}/all-candidates`);
  }

}

