import { OverviewData } from 'Models/Overview';
import { UseQueryResult } from 'react-query';
export declare function useOverviewDataQuery(endpoint?: string | undefined, timeRange?: string | undefined): UseQueryResult<OverviewData, unknown>;
