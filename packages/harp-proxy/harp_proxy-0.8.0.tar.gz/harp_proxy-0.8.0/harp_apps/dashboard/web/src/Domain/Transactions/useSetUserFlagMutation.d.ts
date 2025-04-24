import { UseMutationResult } from 'react-query';
export interface TransactionFlagCreate {
    transactionId: string;
    flag: "favorite";
    value: boolean;
}
export declare function useSetUserFlagMutation(): UseMutationResult<any, unknown, TransactionFlagCreate, unknown>;
