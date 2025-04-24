import { UseQueryResult } from 'react-query';
interface TransactionFilter {
    values: Array<{
        name: string;
        count?: number;
    }>;
    current: string[];
    fallbackName?: string;
}
export declare function useTransactionsFiltersQuery(): UseQueryResult<Record<string, TransactionFilter>, unknown>;
export {};
