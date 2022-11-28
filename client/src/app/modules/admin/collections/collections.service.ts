import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {map, Observable, ReplaySubject, tap} from 'rxjs';
import {environment} from '../../../../environments/environment';
import {Collection} from './collections.types';

@Injectable({
    providedIn: 'root'
})
export class CollectionsService {
    private _collections: ReplaySubject<Collection[]> = new ReplaySubject<Collection[]>();
    private _apiUrl: string = environment.apiUrl + '/api/collections';

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
    get collections$(): Observable<Collection[]> {
        return this._collections.asObservable();
    }

    set collections(value: Collection[]) {
        // Store the value
        this._collections.next(value);
    }

    // -----------------------------------------------------------------------------------------------------
    // @ Public methods
    // -----------------------------------------------------------------------------------------------------

    /**
     * Get get all datasets by username
     */
    get(): Observable<Collection[]> {
        return this._httpClient.get<Collection[]>(`${environment.apiUrl}/api/datasets/features`).pipe(
            tap((datasets) => {
                this._collections.next(datasets);
            })
        );
    }
    /**
     * Get dataset-item by _id
     */
    getById(id: string): Observable<Collection> {
        return this._httpClient.get<Collection>(`${this._apiUrl}/${id}`).pipe(
           map(response => response)
        );
    }
}
