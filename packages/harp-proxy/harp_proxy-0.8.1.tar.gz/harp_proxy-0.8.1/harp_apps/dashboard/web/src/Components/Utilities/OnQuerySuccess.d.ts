import { ReactElement, ReactNode } from 'react';
import { UseQueryResult } from 'react-query';
import { QueryObserverSuccessResult } from 'react-query/types/core/types';
interface OnQuerySuccessCommonProps<T> {
    children: (...queries: QueryObserverSuccessResult<T>[]) => ReactElement;
    onQueryError?: () => void;
}
interface OnQuerySuccessProps<T> extends OnQuerySuccessCommonProps<T> {
    query: UseQueryResult<T>;
}
interface OnQueriesSuccessProps<T> extends OnQuerySuccessCommonProps<T> {
    queries: UseQueryResult<T>[];
}
export declare function OnQuerySuccess<T>(props: (OnQuerySuccessProps<T> | OnQueriesSuccessProps<T>) & {
    fallback?: ReactNode;
}): string | number | boolean | Iterable<ReactNode> | import("@emotion/react/jsx-runtime").JSX.Element | null;
export {};
