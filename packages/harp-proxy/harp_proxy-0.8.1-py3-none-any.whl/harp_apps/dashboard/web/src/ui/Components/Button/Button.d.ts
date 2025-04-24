import { HTMLAttributes, ReactNode } from 'react';
type ButtonVariant = "primary" | "secondary";
interface ButtonProps {
    children?: ReactNode;
    variant?: ButtonVariant;
}
declare const Button: ({ children, variant, ...props }: ButtonProps & HTMLAttributes<HTMLButtonElement>) => import("@emotion/react/jsx-runtime").JSX.Element;
export { Button };
