import axios from "axios";
import { API_CONFIG } from "@/config/api.config";

export const api = axios.create({
    baseURL: API_CONFIG.BASE_URL,
    timeout: API_CONFIG.TIMEOUT,
})

console.log(">>> API CONFIGURADA COM BASE_URL:", API_CONFIG.BASE_URL);

api.interceptors.response.use(
    response => response, (error) => {
        if (error.response){
            console.log('API ERROR', error.response.data);
        }
        return Promise.reject(error);
    }
)