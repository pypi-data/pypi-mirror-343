import { ReactNode } from 'react';
interface FoldableProps {
    open?: boolean;
    title: ReactNode;
    subtitle?: ReactNode;
    children?: ReactNode;
    className?: string;
}
export declare function Foldable({ open, title, subtitle, children, className }: FoldableProps): import("@emotion/react/jsx-runtime").JSX.Element;
export {};
