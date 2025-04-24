declare const SummaryRateChart: ({ data, color, }: {
    data: {
        value: number;
        datetime: string;
    }[];
    color?: string | undefined;
}) => import("@emotion/react/jsx-runtime").JSX.Element;
export default SummaryRateChart;
