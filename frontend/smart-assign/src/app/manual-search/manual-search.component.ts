import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { CandidateService } from '../services/candidate.service';
import { CandidateSummary } from '../models/candidate.model';

@Component({
  selector: 'app-manual-search',
  templateUrl: './manual-search.component.html',
  imports: [CommonModule, FormsModule],
})
export class ManualSearchComponent implements OnInit {
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

  constructor(private readonly candidateService: CandidateService) {}

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


  private parseSkills(skillsStr: string): string[] {
    return skillsStr
      .split(',')
      .map(s => s.trim())
      .filter(s => !!s);
  }

  buildFilterOptions(): void {
    const locs = new Set<string>();
    const grades = new Set<string>();
    const roles = new Set<string>();
    const skills = new Set<string>();

    for (const c of this.manualCandidates) {
      if (c.country) locs.add(c.country);
      if (c.department) grades.add(c.department);           
      if (c.latest_cv_title) roles.add(c.latest_cv_title);
      if (c.skills) {
        for (const s of this.parseSkills(c.skills)) {
          skills.add(s);
        }
      }
    }

    this.manualFilterOptions.locations = ['Any', ...Array.from(locs).sort((a, b) => a.localeCompare(b))];
    this.manualFilterOptions.grades = ['Any', ...Array.from(grades).sort((a, b) => a.localeCompare(b))];
    this.manualFilterOptions.roles = ['Any', ...Array.from(roles).sort((a, b) => a.localeCompare(b))];
    this.manualFilterOptions.skills = ['Any', ...Array.from(skills).sort((a, b) => a.localeCompare(b))];
  }

  private locationMatches(candidate: CandidateSummary): boolean {
    return this.manualLocationFilter === 'Any' || candidate.country === this.manualLocationFilter;
  }

  private gradeMatches(candidate: CandidateSummary): boolean {
    return this.manualGradeFilter === 'Any' || candidate.department === this.manualGradeFilter;
  }

  private scClearanceMatches(candidate: CandidateSummary): boolean {
    if (this.manualScClearanceFilter === 'Any') return true;
    return candidate.clearance === this.manualScClearanceFilter;
  }

  private roleMatches(candidate: CandidateSummary): boolean {
    return this.manualRoleFilter === 'Any' || candidate.latest_cv_title === this.manualRoleFilter;
  }

  private availabilityMatches(candidate: CandidateSummary): boolean {
    switch (this.manualAvailabilityFilter) {
      case 'Any':
        return true;
      case '>= 25%':
        return candidate.availability >= 25;
      case '>= 50%':
        return candidate.availability >= 50;
      case '>= 75%':
        return candidate.availability >= 75;
      default:
        return true;
    }
  }

  private skillsMatches(candidate: CandidateSummary): boolean {
    if (this.manualSkillsFilter === 'Any') return true;
    return candidate.skills?.toLowerCase().includes(this.manualSkillsFilter.toLowerCase()) ?? false;
  }

  applyFilters(): void {
    this.manualFilteredResults = this.manualCandidates.filter(c =>
      this.locationMatches(c) &&
      this.gradeMatches(c) &&
      this.scClearanceMatches(c) &&
      this.roleMatches(c) &&
      this.availabilityMatches(c) &&
      this.skillsMatches(c)
    );
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