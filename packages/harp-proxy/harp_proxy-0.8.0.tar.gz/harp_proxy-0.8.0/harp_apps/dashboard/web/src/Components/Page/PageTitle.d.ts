import { ReactNode } from 'react';
interface PageTitleProps {
    title?: ReactNode;
    description?: string;
    children?: ReactNode;
}
export declare function PageTitle({ description, title, children }: PageTitleProps): import("@emotion/react/jsx-runtime").JSX.Element;
export {};
