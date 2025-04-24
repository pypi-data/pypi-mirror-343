import { OverviewData } from 'Models/Overview';
export interface TransactionsHistoryOnQuerySuccessProps {
    data: OverviewData;
    title?: string;
    className?: string;
}
export declare const TransactionsHistoryOnQuerySuccess: ({ data, title, className, }: TransactionsHistoryOnQuerySuccessProps) => import("@emotion/react/jsx-runtime").JSX.Element;
