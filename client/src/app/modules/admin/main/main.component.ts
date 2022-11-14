import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import TileLayer from 'ol/layer/Tile';
import {XYZ} from 'ol/source';
import {Dataset} from 'app/modules/admin/main/dataset/dataset.types';
import {Subject, takeUntil} from 'rxjs';
import {DatasetService} from './dataset/dataset.service';

@Component({
    selector: 'admin-main',
    templateUrl: './main.component.html',
    styleUrls: ['./main.component.scss'],
    encapsulation: ViewEncapsulation.None
})
export class MainComponent implements OnInit {
    public scaleOptions = {
        units: 'metric',
        bar: true,
        text: true,
        minWidth: 100,
    };
    public layers: any[] = [];
    public datasets: Dataset[] = [];
    private unsubscribeAll: Subject<any> = new Subject<any>();
    /**
     * Constructor
     */
    constructor(
        private datasetService: DatasetService
    ) {
        this.layers = [
            new TileLayer({
                properties: {
                    key: 'mapbox',
                    type: 'bmap',
                    visible: true,
                },
                source: new XYZ({
                    wrapX: false,
                    attributions: '© <a href=\'https://www.mapbox.com/about/maps/\'>Mapbox</a>',
                    url: 'https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw'
                }),
                visible: true
            })
        ];
    }

    ngOnInit(): void {
        this.datasetService.datasets$
            .pipe(takeUntil(this.unsubscribeAll))
            .subscribe((datasets: Dataset[]) => {
                this.datasets = datasets;
            });
    }
}
