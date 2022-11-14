export interface Dataset {
    _id: string;
    file_name: string;
    username: string;
    public: boolean;
    columns: string[];
    epsg: number;
    created_at: Date;
}
