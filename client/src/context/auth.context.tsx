import React, { createContext, useState, useEffect, ReactNode} from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { api } from "@/services/api";
import { AuthService } from "@/services/auth.service";
import { UserService } from "@/services/user.service";
import { AuthResponse, User } from '@/types';

interface AuthContextData{
    user: User | null;
    isLoading: boolean;
    signIn: (email: string, pass: string, remember: boolean) => Promise<void>;
    signInWithToken: (token: string) => Promise<void>;
    signOut: () => void;
}

export const AuthContext = createContext<AuthContextData>({} as AuthContextData);

export const AuthProvider = ({children}: {children: ReactNode}) => {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(()=>{
        localStorageData();
    }, [])

    async function localStorageData(){
        try{
            // SWR: Carrega token e usuário cacheado em paralelo
            const [token, userString] = await Promise.all([
                AsyncStorage.getItem("@Kilocal:token"),
                AsyncStorage.getItem("@Kilocal:user")
            ]);

            if(token){
                api.defaults.headers.common['Authorization'] = `Bearer ${token}`;

                if (userString) {
                    // Hidratação imediata
                    setUser(JSON.parse(userString));
                    setIsLoading(false);
                    // Valida em background
                    revalidateUser();
                } else {
                    // Sem cache, aguarda API
                    await revalidateUser();
                    setIsLoading(false);
                }
            } else {
                setIsLoading(false);
            }
        }catch(error){
            console.log("LocalStorageData ERROR", error);
            setIsLoading(false);
        }
    }

    async function revalidateUser() {
        try {
            const userData = await UserService.getProfile();
            setUser(userData);
            await AsyncStorage.setItem("@Kilocal:user", JSON.stringify(userData));
        } catch(error) {
            console.log("Background revalidate failed", error);
            if ((error as any).response?.status === 401) {
                await signOut();
            }
        }
    }
    
    async function signInWithToken(token: string){
        try{
            await AsyncStorage.setItem("@Kilocal:token", token);
            api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            
            const userData = await UserService.getProfile();
            setUser(userData);
            await AsyncStorage.setItem("@Kilocal:user", JSON.stringify(userData));
        } catch(error){
            console.log("SignInWithToken ERROR", error);
            await signOut();
            throw error;
        }
    }

    async function signIn(email: string, pass: string, remember: boolean){
        const { access_token } = await AuthService.login(email, pass, remember);
        
        await AsyncStorage.setItem("@Kilocal:token", access_token);
        api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

        const userData = await UserService.getProfile();
        setUser(userData);
        await AsyncStorage.setItem("@Kilocal:user", JSON.stringify(userData));
    }

    async function signOut(){
        await AsyncStorage.multiRemove(["@Kilocal:token", "@Kilocal:user"]);
        setUser(null);
        delete api.defaults.headers.common['Authorization'];
    }

    return(
        <AuthContext.Provider value={{user, isLoading, signIn, signInWithToken ,signOut}}>
            {children}
        </AuthContext.Provider>
    )
}