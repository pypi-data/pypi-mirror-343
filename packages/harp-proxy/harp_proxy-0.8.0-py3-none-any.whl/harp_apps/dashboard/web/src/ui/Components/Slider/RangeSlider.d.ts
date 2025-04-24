/// <reference types="react" />
export type Mark = number | {
    value: number;
    label: string;
    className?: string;
};
interface RangeSliderProps {
    min?: number;
    max?: number;
    defaultValue?: {
        min?: number;
        max?: number;
    };
    value?: {
        min?: number;
        max?: number;
    };
    step?: number;
    onChange?: (value: {
        min?: number;
        max?: number;
    }) => void;
    onPointerUp?: (value: {
        min?: number;
        max?: number;
    }) => void;
    thumbSize?: string;
    marks?: Mark[];
}
declare const RangeSlider: React.FC<RangeSliderProps>;
export { RangeSlider };
