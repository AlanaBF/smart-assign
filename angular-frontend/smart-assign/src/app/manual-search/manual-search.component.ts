import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CandidateService } from '../services/candidate.service';
import { CandidateSummary } from '../models/candidate.model';

@Component({
  selector: 'app-manual-search',
  templateUrl: './manual-search.component.html',
  imports: [CommonModule, FormsModule],
})
export class ManualSearchComponent {
  manualCandidates: CandidateSummary[] = [];
  manualFilteredResults: CandidateSummary[] = [];

  manualFilterOptions = {
    locations: [] as string[],
    grades: [] as string[],        
    scClearances: ['Any', 'SC', 'DV', 'NPPV2'],   
    availabilities: ['Any', '>= 25%', '>= 50%', '>= 75%'],
    roles: [] as string[],
    skills: [] as string[],
  };
  isLoading = false;
  error = '';

  manualLocationFilter = 'Any';
  manualGradeFilter = 'Any';
  manualScClearanceFilter = 'Any';
  manualAvailabilityFilter = 'Any';
  manualRoleFilter = 'Any';
  manualSkillsFilter = 'Any';

  constructor(private candidateService: CandidateService) {}

  ngOnInit() {
    this.loadCandidates();
  }

  loadCandidates(): void {
    this.isLoading = true;
    this.candidateService.getAllCandidates().subscribe({
      next: (candidates) => {
        this.manualCandidates = candidates;
        this.manualFilteredResults = [...candidates];
        this.buildFilterOptions();
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Failed to load candidates', err);
        this.isLoading = false;
      }
    });
  }


  buildFilterOptions(): void {
    const locs = new Set<string>();
    const grades = new Set<string>();
    const roles = new Set<string>();
    const skills = new Set<string>();

    this.manualCandidates.forEach(c => {
      if (c.country) locs.add(c.country);
      if (c.department) grades.add(c.department);           
      if (c.latest_cv_title) roles.add(c.latest_cv_title);
      if (c.skills) {
        c.skills.split(',').map(s => s.trim()).forEach(s => {
          if (s) skills.add(s);
        });
      }
    });

    this.manualFilterOptions.locations = ['Any', ...Array.from(locs).sort()];
    this.manualFilterOptions.grades = ['Any', ...Array.from(grades).sort()];
    this.manualFilterOptions.roles = ['Any', ...Array.from(roles).sort()];
    this.manualFilterOptions.skills = ['Any', ...Array.from(skills).sort()];
  }

  applyFilters(): void {
    this.manualFilteredResults = this.manualCandidates.filter(c => {
      if (this.manualLocationFilter !== 'Any' && c.country !== this.manualLocationFilter) {
        return false;
      }
      if (this.manualGradeFilter !== 'Any' && c.department !== this.manualGradeFilter) {
        return false;
      }
      if (this.manualScClearanceFilter !== 'Any') {
        if (this.manualScClearanceFilter === 'SC' && c.clearance !== 'SC') return false;
        if (this.manualScClearanceFilter === 'DV' && c.clearance !== 'DV') return false;
        if (this.manualScClearanceFilter === 'NPPV2' && c.clearance !== 'NPPV2') return false;
      }
      if (this.manualRoleFilter !== 'Any' && c.latest_cv_title !== this.manualRoleFilter) {
        return false;
      }
      if (this.manualAvailabilityFilter === '>= 25%' && c.availability < 25) return false;
      if (this.manualAvailabilityFilter === '>= 50%' && c.availability < 50) return false;
      if (this.manualAvailabilityFilter === '>= 75%' && c.availability < 75) return false;

      if (this.manualSkillsFilter !== 'Any') {
        if (!c.skills?.toLowerCase().includes(this.manualSkillsFilter.toLowerCase())) {
          return false;
        }
      }

      return true;
    });
  }

  onManualLocationFilterChange(value: string) {
    this.manualLocationFilter = value;
    this.applyFilters();
  }
  onManualGradeFilterChange(value: string) {
    this.manualGradeFilter = value;
    this.applyFilters();
  }
  onManualAvailabilityFilterChange(value: string) {
    this.manualAvailabilityFilter = value;
    this.applyFilters();
  }
  onManualRoleFilterChange(value: string) {
    this.manualRoleFilter = value;
    this.applyFilters();
  }
  onManualSkillsFilterChange(value: string) {
    this.manualSkillsFilter = value;
    this.applyFilters();
  }
  onManualScClearanceFilterChange(value: string) {
    this.manualScClearanceFilter = value;
    this.applyFilters();
  }
}