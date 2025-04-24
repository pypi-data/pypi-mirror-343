import { UseQueryResult } from 'react-query';
export interface SummaryData {
    tpdex: {
        mean: number;
        data: {
            datetime: string;
            value: number;
        }[];
    };
    transactions: {
        rate: number;
        period: string;
        data: {
            datetime: string;
            value: number;
        }[];
    };
    errors: {
        rate: number;
        period: string;
        data: {
            datetime: string;
            value: number;
        }[];
    };
}
export declare function useSummaryDataQuery(): UseQueryResult<SummaryData, unknown>;
