import axios from 'axios'

const apiClient = axios.create({
    baseURL: 'http://localhost:24990',
    timeout: 10000,
    headers: "/application/json"
})

// 响应拦截器
apiClient.interceptors.request.use(
    (response) => response,
    error => {
        console.error(error)
        return Promise.reject(error)
    })

export default apiClient