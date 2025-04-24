interface SearchBarProps {
    label?: string;
    placeHolder?: string;
    setSearch?: (value: string) => void;
    className?: string;
    search?: string | null;
}
export declare const SearchBar: ({ label, setSearch, className, placeHolder, search }: SearchBarProps) => import("@emotion/react/jsx-runtime").JSX.Element;
export {};
