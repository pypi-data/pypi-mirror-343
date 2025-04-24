import { Transaction } from 'Models/Transaction';
export interface TransactionsDataTableProps {
    transactions: Transaction[];
    onSelectionChange?: (selected: Transaction | null) => void;
    selected?: Transaction;
}
export declare function TransactionDataTable({ transactions, onSelectionChange, selected }: TransactionsDataTableProps): import("@emotion/react/jsx-runtime").JSX.Element;
