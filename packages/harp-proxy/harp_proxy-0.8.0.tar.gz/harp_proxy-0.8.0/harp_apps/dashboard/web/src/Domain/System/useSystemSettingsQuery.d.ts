import { UseQueryResult } from 'react-query';
export interface KeyValueSettings {
    [key: string]: Setting;
}
export type Setting = string | number | boolean | null | KeyValueSettings | Array<Setting>;
export declare function useSystemSettingsQuery(): UseQueryResult<KeyValueSettings, unknown>;
