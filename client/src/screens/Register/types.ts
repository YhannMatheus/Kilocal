export interface RegisterForms{
    name: string;
    email: string;
    password: string;
    confirmPassword: string;
    dayOfBirth: string;
    monthOfBirth: string;
    yearOfBirth: string;
    height: number;
    gender: "male" | "female";
}

export interface RegisterErrors{
    name?: string;
    email?: string;
    password?: string;
    confirmPassword?: string;
    dayOfBirth?: string;
    monthOfBirth?: string;
    yearOfBirth?: string;
    height?: string;
    gender?: string;
}