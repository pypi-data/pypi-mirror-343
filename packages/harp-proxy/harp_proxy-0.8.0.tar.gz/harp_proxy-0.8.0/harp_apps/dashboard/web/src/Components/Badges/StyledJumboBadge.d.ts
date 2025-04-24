import { StyledComponent } from '@emotion/styled';
import { Theme } from '@emotion/react';
import { ElementType, DetailedHTMLProps, HTMLAttributes } from 'react';
/// <reference types="react" />
export interface StyledJumboBadgeProps {
    size?: "xs" | "sm" | "md" | "lg" | "xl";
    color?: "black" | "white";
}
export declare const StyledJumboBadge: StyledComponent<{
    theme?: Theme | undefined;
    as?: ElementType<any, keyof import("react").JSX.IntrinsicElements> | undefined;
} & StyledJumboBadgeProps, DetailedHTMLProps<HTMLAttributes<HTMLSpanElement>, HTMLSpanElement>, {}>;
