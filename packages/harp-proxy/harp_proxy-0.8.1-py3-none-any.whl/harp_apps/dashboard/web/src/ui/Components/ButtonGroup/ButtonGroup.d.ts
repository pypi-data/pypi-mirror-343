interface ButtonProp {
    key: string;
    title: string;
}
type ButtonProps = Array<ButtonProp>;
export declare function ButtonGroup({ buttonProps, current, setCurrent, }: {
    buttonProps: ButtonProps;
    current: string;
    setCurrent: (current: string) => void;
}): import("@emotion/react/jsx-runtime").JSX.Element;
export {};
