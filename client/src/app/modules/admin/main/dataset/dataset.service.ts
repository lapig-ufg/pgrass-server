import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {map, Observable, ReplaySubject, tap} from 'rxjs';
import {Dataset} from './dataset.types';
import {environment} from '../../../../../environments/environment';

@Injectable({
    providedIn: 'root'
})
export class DatasetService {
    private _dataset: ReplaySubject<Dataset> = new ReplaySubject<Dataset>(1);
    private _datasets: ReplaySubject<Dataset[]> = new ReplaySubject<Dataset[]>();
    private _apiUrl: string = environment.apiUrl + '/api/dataset';

    /**
     * Constructor
     */
    constructor(private _httpClient: HttpClient) {
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Accessors
    // -----------------------------------------------------------------------------------------------------


    /**
     * Setter & getter for user
     *
     * @param value
     */
    get datasets$(): Observable<Dataset[]> {
        return this._datasets.asObservable();
    }

    set datasets(value: Dataset[]) {
        // Store the value
        this._datasets.next(value);
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Public methods
    // -----------------------------------------------------------------------------------------------------

    /**
     * Get get all datasets by username
     */
    get(): Observable<Dataset[]> {
        return this._httpClient.get<Dataset[]>(`${this._apiUrl}/`).pipe(
            tap((datasets) => {
                this._datasets.next(datasets);
            })
        );
    }
    /**
     * Get dataset by _id
     */
    getById(id: string): Observable<Dataset> {
        return this._httpClient.get<Dataset>(`${this._apiUrl}/${id}`).pipe(
            tap((user) => {
                this._dataset.next(user);
            })
        );
    }
}
