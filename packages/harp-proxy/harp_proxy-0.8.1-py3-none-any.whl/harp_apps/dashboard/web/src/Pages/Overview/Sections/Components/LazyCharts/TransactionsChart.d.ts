import { OverviewTransaction } from 'Models/Overview';
interface TransactionsChartProps {
    data: Array<OverviewTransaction>;
    timeRange?: string;
}
declare const TransactionsChart: ({ data, timeRange }: TransactionsChartProps) => import("@emotion/react/jsx-runtime").JSX.Element;
export default TransactionsChart;
