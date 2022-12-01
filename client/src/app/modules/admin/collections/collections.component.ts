import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import TileLayer from 'ol/layer/Tile';
import {XYZ} from 'ol/source';
import {Subject, takeUntil} from 'rxjs';
import {CollectionsService} from './collections.service';
import {MatDialog} from '@angular/material/dialog';
import {Collection} from './collections.types';

@Component({
    selector: 'collections',
    templateUrl: './collections.component.html',
    styleUrls: ['./collections.component.scss'],
    encapsulation: ViewEncapsulation.None
})
export class CollectionsComponent implements OnInit {
    public layers: any[] = [];
    public collections: Collection[] = [];
    private unsubscribeAll: Subject<any> = new Subject<any>();

    /**
     * Constructor
     */
    constructor(
        private collectionsService: CollectionsService,
        public dialog: MatDialog
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
        this.loadCollections();
    }

    loadCollections(): void {
        this.collectionsService.collections$
            .pipe(takeUntil(this.unsubscribeAll))
            .subscribe((collections: Collection[]) => {
                this.collections = collections;
            });
    }
}
