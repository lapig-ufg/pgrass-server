import {Component, ViewEncapsulation} from '@angular/core';
import TileLayer from 'ol/layer/Tile';
import {XYZ} from "ol/source";

@Component({
    selector: 'example',
    templateUrl: './example.component.html',
    encapsulation: ViewEncapsulation.None
})
export class ExampleComponent {
    public scaleOptions = {
        units: 'metric',
        bar: true,
        text: true,
        minWidth: 100,
    };
    public layers: any[] = [];

    /**
     * Constructor
     */
    constructor() {
        this.layers = [
            {
                layer: new TileLayer({
                    properties: {
                        key: 'mapbox',
                        type: 'bmap',
                        visible: true,
                    },
                    source: new XYZ({
                        wrapX: false,
                        url:
                            'https://api.mapbox.com/styles/v1/mapbox/light-v10/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw'
                    }),
                    visible: true
                })
            }
        ];
    }
}
