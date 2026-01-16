export type ActivityLevel =
    | 'sedentary'
    | 'lightly_active'
    | 'moderately_active'
    | 'very_active'
    | 'extra_active';

export type Gender = 'male' | 'female';

export interface User{
    id: string;
    name: string;
    email: string;
    gender: Gender
    birthDate: string;
    heigth : number;
    weigth : number;
    activityLevel: ActivityLevel;
}

export interface AuthResponse{
    access_token: string;
    token_type: string;
}

export type RootStackParamList = {
  Login: undefined;
  Register: undefined;
  Dashboard: undefined;
};