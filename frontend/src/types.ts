export type Data = {
    result: Array<{ [key: string]: string | number }>;
};


export interface ExecutionStep {
    Id: string;
    Operation: string;
    Name: string;
    Rows: number;
    Bytes: number;
    Cost: string;
    Time: string;
}