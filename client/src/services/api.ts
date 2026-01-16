import axios from "axios";

export const api = axios.create({
    baseURL: 'http://localhost:3000/api',
})

api.interceptors.request.use(
    response => response, (error) => {
        if (error.response){
            console.log('API ERROR', error.response.data);
        }
        return Promise.reject(error);
    }
)