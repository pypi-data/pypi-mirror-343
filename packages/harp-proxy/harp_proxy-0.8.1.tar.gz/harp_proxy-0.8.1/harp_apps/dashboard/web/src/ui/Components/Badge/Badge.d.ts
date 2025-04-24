import { StyledComponent } from '@emotion/styled';
import { Theme } from '@emotion/react';
import { ElementType, DetailedHTMLProps, HTMLAttributes } from 'react';
/// <reference types="react" />
export type BadgeColor = "default" | "green" | "yellow" | "orange" | "red" | "blue" | "purple";
interface BadgeProps {
    color?: BadgeColor;
}
export declare const Badge: StyledComponent<{
    theme?: Theme | undefined;
    as?: ElementType<any, keyof import("react").JSX.IntrinsicElements> | undefined;
} & BadgeProps, DetailedHTMLProps<HTMLAttributes<HTMLSpanElement>, HTMLSpanElement>, {}>;
export {};
