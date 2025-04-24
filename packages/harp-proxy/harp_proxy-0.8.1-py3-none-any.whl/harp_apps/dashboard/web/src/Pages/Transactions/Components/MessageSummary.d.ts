interface MessageSummaryProps {
    kind?: string;
    summary?: string;
    endpoint?: string;
}
export declare const RequestMessageSummary: ({ method, url, endpoint, }: {
    method: string;
    url: string;
    endpoint?: string | undefined;
}) => import("@emotion/react/jsx-runtime").JSX.Element;
export declare function MessageSummary({ kind, summary, endpoint }: MessageSummaryProps): import("@emotion/react/jsx-runtime").JSX.Element;
export {};
