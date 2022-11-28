import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import TileLayer from 'ol/layer/Tile';
import {XYZ} from 'ol/source';
import {Dataset} from 'app/modules/admin/datasets/datasets.types';
import {Subject, takeUntil} from 'rxjs';
import {DatasetsService} from './datasets.service';
import {UploaderConfig} from '../../../core/uploader/uploader.types';
import {AuthService} from '../../../core/auth/auth.service';
import {environment} from "../../../../environments/environment";
import {MatDialog} from "@angular/material/dialog";
import {UploadDatasetDialogComponent} from "./upload-dataset-dialog/upload-dataset-dialog.component";

@Component({
    selector: 'admin-datasets',
    templateUrl: './datasets.component.html',
    styleUrls: ['./datasets.component.scss'],
    encapsulation: ViewEncapsulation.None
})
export class DatasetsComponent implements OnInit {
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
        private datasetService: DatasetsService,
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
        this.loadDatasets();
    }

    loadDatasets(): void {
        this.datasetService.datasets$
            .pipe(takeUntil(this.unsubscribeAll))
            .subscribe((datasets: Dataset[]) => {
                console.log('datasets', datasets);
                this.datasets = datasets;
            });
    }

    openUploader(): void {
        const dialogRef = this.dialog.open(UploadDatasetDialogComponent);
        dialogRef.afterClosed().subscribe((fileCreated) => {
            if(fileCreated){
                console.log(fileCreated);
                this.loadDatasets();
            }
        });
    }
}
