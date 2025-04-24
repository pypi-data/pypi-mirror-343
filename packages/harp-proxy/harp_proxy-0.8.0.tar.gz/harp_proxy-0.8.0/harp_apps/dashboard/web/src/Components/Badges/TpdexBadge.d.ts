import { ReactNode } from 'react';
import { StyledJumboBadgeProps } from './StyledJumboBadge.tsx';
export default function TpdexBadge({ score, className, children, ...styledProps }: {
    score?: number;
    className?: string;
    children?: ReactNode;
} & StyledJumboBadgeProps): import("@emotion/react/jsx-runtime").JSX.Element | null;
