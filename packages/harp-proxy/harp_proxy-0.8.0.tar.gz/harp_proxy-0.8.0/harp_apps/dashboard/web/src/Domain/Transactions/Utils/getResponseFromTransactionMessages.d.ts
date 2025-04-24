import { Message, Transaction } from 'Models/Transaction';
export declare const getResponseFromTransactionMessages: (transation: Transaction) => {
    response?: Message;
    error?: Message;
    endpoint?: string;
};
