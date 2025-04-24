import { UseQueryResult, UseMutationResult } from 'react-query';
export declare function useSystemProxyQuery(): UseQueryResult<{
    endpoints: Apps.Proxy.Endpoint[];
}, unknown>;
export declare function useSystemProxyMutation(): UseMutationResult<any, unknown, {
    endpoint: string;
    action: string;
    url: string;
}, unknown>;
