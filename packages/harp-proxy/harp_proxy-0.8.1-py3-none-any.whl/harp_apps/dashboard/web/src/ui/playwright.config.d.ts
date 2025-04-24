declare const _default: {
    timeout: number;
    use: {
        baseURL: string;
    };
    reporter: string[][];
    webServer: {
        command: string;
        env: {
            NODE_ENV: string;
        };
        url: string;
        reuseExistingServer: boolean;
    };
    retries: number;
    testMatch: string;
};
export default _default;
