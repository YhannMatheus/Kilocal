import React, { createContext, useState, useEffect, ReactNode} from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { api } from "@/services/api";
import {AuthResponse, User} from '@/types';

interface AuthContextData{
    user: User | null;
    isLoading: boolean;
    signIn: (email: string, pass: string, remember: boolean) => Promise<void>;
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
            const token = await AsyncStorage.getItem("@Kilocal:token");

            if(token){
                api.defaults.headers.common['Authorization'] = `Bearer ${token}`;

                try{
                    const response = await api.get<User>('/users/me');
                    setUser(response.data);
                }catch(error){
                    await signOut();
                }
            }
        }catch(error){
            console.log("LocalStorageData ERROR", error);
        }finally{
            setIsLoading(false);
        }
    }

    async function signIn(email: string, pass: string, remember: boolean){
        const response = await api.post<AuthResponse>('/user/login', {
            email,
            password: pass
        })

        const {access_token} = response.data;
        await AsyncStorage.setItem("@Kilocal:token", access_token);
        api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;

        const userResponse = await api.get<User>('/users/me');
        setUser(userResponse.data);
    }
    async function signOut(){
        await AsyncStorage.removeItem("@Kilocal:token");
        setUser(null);
        delete api.defaults.headers.common['Authorization'];
    }

    return(
        <AuthContext.Provider value={{user, isLoading, signIn, signOut}}>
            {children}
        </AuthContext.Provider>
    )
}