import { Message, Transaction } from 'Models/Transaction';
export declare const getRequestFromTransactionMessages: (transaction: Transaction) => {
    request?: Message;
    endpoint?: string;
};
