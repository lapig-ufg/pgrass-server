import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {OlMapsModule} from './map/ol-maps.module';

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        ReactiveFormsModule,
        OlMapsModule
    ],
    exports: [
        CommonModule,
        FormsModule,
        ReactiveFormsModule,
        OlMapsModule
    ]
})
export class SharedModule
{
}
