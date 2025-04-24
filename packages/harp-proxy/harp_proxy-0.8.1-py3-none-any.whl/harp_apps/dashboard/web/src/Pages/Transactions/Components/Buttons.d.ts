import { HTMLAttributes } from 'react';
interface ButtonProps {
    onClick?: () => unknown;
}
export declare function VerticalFiltersShowButton({ onClick }: ButtonProps): import("@emotion/react/jsx-runtime").JSX.Element;
export declare function FiltersHideButton({ onClick }: ButtonProps): import("@emotion/react/jsx-runtime").JSX.Element;
export declare function FiltersResetButton({ onClick }: ButtonProps): import("@emotion/react/jsx-runtime").JSX.Element;
export declare function DetailsCloseButton({ onClick, ...moreProps }: ButtonProps & HTMLAttributes<HTMLButtonElement>): import("@emotion/react/jsx-runtime").JSX.Element;
export declare function PreviousButton({ onClick }: ButtonProps): import("@emotion/react/jsx-runtime").JSX.Element;
export declare function NextButton({ onClick }: ButtonProps): import("@emotion/react/jsx-runtime").JSX.Element;
export declare function RefreshButton({ onClick, ...moreProps }: ButtonProps & HTMLAttributes<HTMLButtonElement>): import("@emotion/react/jsx-runtime").JSX.Element;
export declare function OpenInNewWindowLink({ id }: {
    id: string;
}): import("@emotion/react/jsx-runtime").JSX.Element;
export {};
