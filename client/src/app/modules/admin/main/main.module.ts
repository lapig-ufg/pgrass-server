import { NgModule } from '@angular/core';
import {CommonModule} from '@angular/common';
import { Route, RouterModule } from '@angular/router';
import { MainComponent } from 'app/modules/admin/main/main.component';
import {OlMapsModule} from '../../../shared/map/ol-maps.module';
import {TranslocoModule} from '@ngneat/transloco';
import {FuseCardModule} from "../../../../@fuse/components/card";
import {FuseDrawerModule} from "../../../../@fuse/components/drawer";

const exampleRoutes: Route[] = [
    {
        path     : '',
        component: MainComponent
    }
];

@NgModule({
    declarations: [
        MainComponent
    ],
    imports: [
        CommonModule,
        RouterModule.forChild(exampleRoutes),
        OlMapsModule,
        TranslocoModule,
        FuseCardModule,
        FuseDrawerModule
    ]
})
export class MainModule
{
}
