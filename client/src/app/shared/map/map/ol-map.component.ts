import {
    Component,
    OnInit,
    AfterViewInit,
    Input,
    ElementRef,
    Output,
    EventEmitter,
    ChangeDetectorRef,
    HostListener, OnChanges, SimpleChanges
} from '@angular/core';
import 'ol/ol.css';
import Map from 'ol/Map';
import View from 'ol/View';
import {defaults as defaultInteractions} from 'ol/interaction';
import * as Proj from 'ol/proj';

export const DEFAULT_WIDTH = '100%';
export const DEFAULT_HEIGHT = '500px';

export const DEFAULT_LAT = -34.603490361131385;
export const DEFAULT_LON = -58.382037891217465;

@Component({
    selector: 'ol-map',
    templateUrl: './ol-map.component.html',
    styleUrls: ['./ol-map.component.scss']
})
export class OlMapComponent implements OnInit, AfterViewInit, OnChanges {

    @Input() lat: number = DEFAULT_LAT;
    @Input() lon: number = DEFAULT_LON;
    @Input() loading: boolean = false;
    @Input() zoom: number;
    @Input() width: string | number = DEFAULT_WIDTH;
    @Input() height: string | number = DEFAULT_HEIGHT;
    @Output() ready = new EventEmitter<Map>();
    public target: string = '';
    map: Map;

    private mapEl: HTMLElement;

    constructor(private elementRef: ElementRef, private cdRef: ChangeDetectorRef) {

    }

    @HostListener('window:resize', ['$event'])
    onWindowResize(): void {
        this.map.updateSize();
    }

    ngOnInit(): void {
        this.target = 'map-' + Math.random().toString(36).substring(2);
    }

    ngAfterViewInit(): void {
        const self = this;
        this.mapEl = this.elementRef.nativeElement.querySelector('#' + this.target);
        this.setSize();
        this.map = new Map({
            target: this.target,
            interactions: defaultInteractions({altShiftDragRotate: false, pinchRotate: false}),
            view: new View({
                center: Proj.fromLonLat([this.lon, this.lat]),
                zoom: this.zoom
            })
        });
        this.map.on('postrender', () => {
            self.loading = false;
        });
        this.cdRef.detectChanges();
        setTimeout(() => {
            this.ready.emit(this.map);
        });
    }

    ngOnChanges(changes: SimpleChanges): void {
        // console.log(changes);
    }

    setSize(): void {
        if (this.mapEl) {
            const styles = this.mapEl.style;
            styles.height = this.coerceCssPixelValue(this.height) || DEFAULT_HEIGHT;
            styles.width = this.coerceCssPixelValue(this.width) || DEFAULT_WIDTH;
        }
    }

    public addLayer(layer): void {
        this.map.addLayer(layer);
        this.cdRef.detectChanges();
    }

    setMarker(vector): void {
        this.map.addLayer(vector);
        this.cdRef.detectChanges();
    }

    public setControl(control: any): void {
        this.map.addControl(control);
    }

    coerceCssPixelValue(value: any): string {
        const cssUnitsPattern = /([A-Za-z%]+)$/;
        if (value == null) {
            return '';
        }
        return cssUnitsPattern.test(value) ? value : `${value}px`;
    }
}

