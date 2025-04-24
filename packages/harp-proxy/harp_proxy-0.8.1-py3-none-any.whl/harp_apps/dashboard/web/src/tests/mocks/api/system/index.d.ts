import { HttpHandler } from 'msw';
declare const _default: HttpHandler & {
    dependencies: HttpHandler;
    settings: HttpHandler;
    storage: HttpHandler;
    proxy: HttpHandler;
};
export default _default;
