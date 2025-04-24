import { UseQueryResult } from 'react-query';
export declare function useSystemQuery(): UseQueryResult<{
    version: string;
    revision: string;
    user?: string | null | undefined;
}, unknown>;
