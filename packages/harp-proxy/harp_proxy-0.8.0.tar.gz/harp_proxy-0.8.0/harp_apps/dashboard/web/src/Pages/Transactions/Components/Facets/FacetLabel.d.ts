import { ReactNode } from 'react';
interface FacetLabelProps {
    name: string;
    count?: number;
    children?: ReactNode;
}
export declare function FacetLabel({ name, count, children }: FacetLabelProps): import("@emotion/react/jsx-runtime").JSX.Element;
export {};
