import { api } from "./api";
import { User } from "@/types";

export const UserService = {
    async getProfile() {
        // Correção da rota (singular)
        const response = await api.get<User>('/user/profile');
        return response.data;
    },

    async register(data: any) {
        const response = await api.post('/user/register', data);
        return response.data;
    }
}
