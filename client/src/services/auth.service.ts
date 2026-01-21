import { api } from "./api";
import { AuthResponse } from "@/types";

export const AuthService = {
    async login(email: string, pass: string, remember: boolean) {
        const response = await api.post<AuthResponse>('/user/login', {
            email,
            password: pass,
            remember
        });
        return response.data;
    }
}
