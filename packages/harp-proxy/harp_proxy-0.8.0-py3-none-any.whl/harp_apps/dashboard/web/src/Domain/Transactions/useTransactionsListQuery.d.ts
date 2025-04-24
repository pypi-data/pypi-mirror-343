import { ItemList } from 'Domain/Api/Types';
import { Transaction } from 'Models/Transaction';
import { Filters } from 'Types/filters';
import { UseQueryResult } from 'react-query';
export declare function useTransactionsListQuery({ page, cursor, filters, search, }: {
    filters?: Filters;
    page?: number;
    cursor?: string | null;
    search?: string | null;
}): UseQueryResult<ItemList<Transaction> & {
    total: number;
    pages: number;
    perPage: number;
}, unknown>;
