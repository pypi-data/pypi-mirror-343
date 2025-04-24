import { ArrayFilter } from 'Types/filters';
interface FacetProps {
    title: string;
    name: string;
    type: "checkboxes" | "radios";
    defaultOpen?: boolean;
    meta: Array<{
        name: string;
        count?: number;
    }>;
    values?: ArrayFilter;
    setValues?: (value: ArrayFilter) => unknown;
    fallbackName?: string;
}
/**
 * Facet component, renders a facet (group of values that can filter a given field) with checkboxes or radios.
 *
 * Radios for single selection, checkboxes for multiple selection. La base.
 */
export declare function Facet({ title, name, values, setValues, meta, type, defaultOpen, fallbackName, }: FacetProps): import("@emotion/react/jsx-runtime").JSX.Element;
export {};
