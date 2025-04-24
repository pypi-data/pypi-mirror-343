import { Transaction } from 'Models/Transaction';
import { UseQueryResult } from 'react-query';
export declare function useTransactionsDetailQuery(id?: string): UseQueryResult<Transaction, unknown>;
