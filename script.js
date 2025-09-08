import http from 'k6/http';
import { sleep } from 'k6';
// import * as config from './config.js';
export const options = {
    vus: 1,
    duration: '30s',
    thresholds: {
        http_req_duration: ['p(95)<1000']
    },
};
export default function () {
    http.get('http://localhost:8001/saludo');
    sleep(1);
}