export enum BioStatusType {
    BFP = "bfp",
    TDEE = "tdee",
    WEIGHT = "weight",
    BMI = "bmi",
    BMR = "bmr",
    LEAN_FAT_MASS = "lean_fat_mass"
}

export interface GraphPoint {
    date: string;
    value: number;
}