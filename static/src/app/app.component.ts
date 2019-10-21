import {Component, ElementRef, ViewChild} from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'static';

  @ViewChild('scrollMe', {static: false}) private myScrollContainer: ElementRef;

  constructor() {

  }


  onScroll(): void {
    const scrollY = this.myScrollContainer.nativeElement.scrollTop;

    if (scrollY <= 400) {
      document.getElementById("navbar").style.top = "-80px";
    } else {
      document.getElementById("navbar").style.top = "0";
    }
  }
}
