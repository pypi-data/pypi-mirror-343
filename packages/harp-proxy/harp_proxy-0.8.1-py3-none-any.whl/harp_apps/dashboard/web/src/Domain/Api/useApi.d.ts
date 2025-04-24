export declare function useApi(): {
    fetch: (url: string) => Promise<Response>;
    get: (url: string, init?: RequestInit) => Promise<Response>;
    post: (url: string, init?: RequestInit) => Promise<Response>;
    del: (url: string, init?: RequestInit) => Promise<Response>;
    put: (url: string, init?: RequestInit) => Promise<Response>;
};
