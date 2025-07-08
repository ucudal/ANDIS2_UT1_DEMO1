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
    http.get('http://127.0.0.1:5000/saludo');
    sleep(1);
}