import { UseQueryResult } from 'react-query';
interface Blob {
    id: string;
    content: ArrayBuffer;
    contentType?: string;
}
export declare function useBlobQuery(id?: string): UseQueryResult<Blob | undefined, unknown>;
export {};
