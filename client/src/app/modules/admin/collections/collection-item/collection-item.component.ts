import {Component, Input, OnInit, ViewEncapsulation} from '@angular/core';
import TileLayer from 'ol/layer/Tile';
import {XYZ} from 'ol/source';
import {MatDialog} from '@angular/material/dialog';
import {Collection} from '../collections.types';
import {Router} from '@angular/router';

@Component({
    selector: 'collection-item',
    templateUrl: './collection-item.component.html',
    styleUrls: ['./collection-item.component.scss'],
    encapsulation: ViewEncapsulation.None
})
export class CollectionItemComponent implements OnInit {
    public layers: any[] = [];
    public _collection: Collection;
    /**
     * Constructor
     */
    constructor(
        public dialog: MatDialog,
                private router: Router

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

    @Input() set collection(value: Collection) {
        if (value) {
            this._collection = value;
        }
    };

    ngOnInit(): void {
    }

    async analyze(): Promise<any>{
        await this.router.navigate(['/collections/analyze', { datasetId: this._collection._id }]);
    }
}
