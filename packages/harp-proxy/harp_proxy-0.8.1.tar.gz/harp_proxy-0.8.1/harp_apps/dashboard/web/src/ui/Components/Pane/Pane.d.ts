import { StyledComponent } from '@emotion/styled';
import { Theme } from '@emotion/react';
import { ElementType, DetailedHTMLProps, HTMLAttributes } from 'react';
/// <reference types="react" />
export declare const Pane: StyledComponent<{
    theme?: Theme | undefined;
    as?: ElementType<any, keyof import("react").JSX.IntrinsicElements> | undefined;
} & {
    hasDefaultPadding?: boolean | undefined;
    hasDefaultBorder?: boolean | undefined;
}, DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement>, {}>;
