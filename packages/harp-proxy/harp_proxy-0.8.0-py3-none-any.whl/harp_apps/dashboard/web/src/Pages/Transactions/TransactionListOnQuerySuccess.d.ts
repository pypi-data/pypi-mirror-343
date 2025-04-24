import { QueryObserverSuccessResult } from 'react-query/types/core/types';
import { ItemList } from 'Domain/Api/Types';
import { Transaction } from 'Models/Transaction';
import { Filters } from 'Types/filters';
import { TransactionsDataTableProps } from './Components/List/TransactionDataTable.tsx';
export declare function TransactionListOnQuerySuccess({ query, filters, TransactionDataTable, }: {
    query: QueryObserverSuccessResult<ItemList<Transaction> & {
        total: number;
        pages: number;
        perPage: number;
    }>;
    filters: Filters;
    TransactionDataTable: React.FC<TransactionsDataTableProps>;
}): import("@emotion/react/jsx-runtime").JSX.Element;
