import axios from "axios";

export const api = axios.create({
    baseURL: 'https://kilocal-8fy9.onrender.com/api/v1',
})

api.interceptors.request.use(
    response => response, (error) => {
        if (error.response){
            console.log('API ERROR', error.response.data);
        }
        return Promise.reject(error);
    }
)