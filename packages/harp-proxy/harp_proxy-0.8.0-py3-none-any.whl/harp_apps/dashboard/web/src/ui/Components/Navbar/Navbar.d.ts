import { ComponentType, ReactElement, ReactNode } from 'react';
import { To } from 'react-router-dom';
interface NavbarItem {
    label: string;
    to: string;
    exact?: boolean;
}
interface NavbarProps {
    Link?: ComponentType<{
        children?: ReactNode;
        to: To;
        className?: string;
    }>;
    Wrapper?: ComponentType<{
        children?: ReactNode;
    }>;
    items?: NavbarItem[];
    currentPath?: string;
    leftChildren?: ReactElement;
    rightChildren?: ReactElement;
    className?: string;
}
declare function Navbar({ Link, Wrapper, items, currentPath, leftChildren, rightChildren, className, }: NavbarProps): import("@emotion/react/jsx-runtime").JSX.Element;
export { Navbar };
