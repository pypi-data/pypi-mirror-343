import { ReactNode } from 'react';
import { FallbackProps } from 'react-error-boundary';
export declare function Error(props: FallbackProps): import("@emotion/react/jsx-runtime").JSX.Element;
interface PageProps {
    children: ReactNode;
    title?: ReactNode;
}
export declare function Page({ children, title }: PageProps): import("@emotion/react/jsx-runtime").JSX.Element;
export {};
