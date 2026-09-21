import axios from 'axios'

export const assetBaseUrl = import.meta.env.VITE_ASSET_BASE_URL || 'http://localhost:24999';

export const remoteApi = axios.create({
    baseURL: 'http://localhost:24990',
    timeout: 10000,
    headers: "/application/json",
});

export const localApi = axios.create({
    baseURL: 'http://localhost:24999',
    timeout: 10000,
    headers: "/application/json",
});

// 响应拦截器
remoteApi.interceptors.request.use(
    (response) => response,
    error => {
        console.error(error);
        return Promise.reject(error);
    })

localApi.interceptors.request.use(
    (response) => response,
    error => {
        console.log(error);
        return Promise.reject(error);
    }
)