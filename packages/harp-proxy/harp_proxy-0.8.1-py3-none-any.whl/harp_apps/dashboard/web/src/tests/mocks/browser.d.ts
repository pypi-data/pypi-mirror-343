import { http, HttpResponse } from 'msw';
import { SetupWorker } from 'msw/browser';
declare const worker: SetupWorker;
export { worker, http, HttpResponse };
