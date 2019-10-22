import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { MaterialModule } from './material.module';
import { FlexLayoutModule } from '@angular/flex-layout';

@NgModule({
  declarations: [
  ],
  imports: [
    FlexLayoutModule,
    MaterialModule,
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  exports: [
    FlexLayoutModule,
    MaterialModule,
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  entryComponents: [
  ],
  providers: [
  ]
})

export class SharedModule {

}
