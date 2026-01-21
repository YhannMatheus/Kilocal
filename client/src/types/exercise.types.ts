export enum TrainingType {
    STRENGTH = "strength",
    CARDIO = "cardio",
    FLEXIBILITY = "flexibility",
    SPORTS = "sports",
    CROSSFIT = "crossfit"
}

export enum MuscleGroup {
    BACK = "back",
    CHEST = "chest",
    LEGS = "legs",
    ARMS = "arms",
    SHOULDERS = "shoulders",
    ABDOMEN = "abdomen",
    CARDIO = "cardio"
}

export interface Exercise {
    id: string;
    name: string;
    target_muscle: MuscleGroup;
    instructions?: string;
    is_system_default: boolean;
}
