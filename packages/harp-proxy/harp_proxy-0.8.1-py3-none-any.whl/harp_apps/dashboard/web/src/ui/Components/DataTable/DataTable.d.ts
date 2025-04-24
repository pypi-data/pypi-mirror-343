import { ReactNode } from 'react';
export interface Column<TRow = unknown, TValue = unknown> {
    label: string;
    format?: (row: never) => ReactNode;
    get?: (row: TRow) => TValue;
    onClick?: (row: TRow) => unknown;
    className?: string;
    headerClassName?: string;
}
interface DataTableVariantsProps {
    variant?: "default";
}
type BaseRow = Record<string, unknown>;
interface DataTableProps<TRow extends BaseRow, TComputed extends BaseRow> extends DataTableVariantsProps {
    rows: TRow[];
    types: Record<string, Column<TRow>>;
    columns?: Array<keyof (TRow & TComputed) | Array<keyof (TRow & TComputed)>>;
    onRowClick?: (row: TRow) => unknown;
    selected?: TRow;
    rowKey?: string;
}
export declare function DataTable<TRow extends BaseRow, TComputed extends BaseRow = BaseRow>({ columns, onRowClick, rows, types, variant, selected, rowKey, }: DataTableProps<TRow, TComputed>): import("@emotion/react/jsx-runtime").JSX.Element;
export {};
