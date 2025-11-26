import { Component } from '@angular/core';
import { ManualSearchComponent } from '../manual-search/manual-search.component';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home-page',
  standalone: true,
  imports: [CommonModule, ManualSearchComponent],
  templateUrl: './home-page.component.html',
})
export class HomePageComponent {
}
