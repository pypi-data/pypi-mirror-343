import { MinMaxFilter } from 'Types/filters';
import { Mark } from '../../../../ui/Components/Slider/RangeSlider.tsx';
interface RangeSliderFacetProps {
    title: string;
    name: string;
    defaultOpen?: boolean;
    values?: MinMaxFilter;
    setValues: (value?: MinMaxFilter) => void;
    marks?: Mark[];
    min?: number;
    max?: number;
}
export declare function RangeSliderFacet({ title, name, values, setValues, defaultOpen, marks, min, max, }: RangeSliderFacetProps): import("@emotion/react/jsx-runtime").JSX.Element;
export {};
