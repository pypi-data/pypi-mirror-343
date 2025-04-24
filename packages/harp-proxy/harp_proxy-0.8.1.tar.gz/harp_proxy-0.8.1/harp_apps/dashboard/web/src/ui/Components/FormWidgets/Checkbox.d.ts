import { ReactNode } from 'react';
export declare function Checkbox({ name, label, checked, containerProps, labelProps, disabled, ...inputProps }: {
    name: string;
    label?: string | ReactNode;
    checked?: boolean;
    containerProps?: React.HTMLAttributes<HTMLDivElement>;
    labelProps?: React.HTMLAttributes<HTMLLabelElement>;
    disabled?: boolean;
} & React.HTMLAttributes<HTMLInputElement>): import("@emotion/react/jsx-runtime").JSX.Element;
