export interface WorkoutCreate {
    userId: string;
    name : string;
    type : "cardio" | "strength" | "flexibility" | "balance";
    startTime: string;
}

export interface WorkoutRead {
    id : string;
    userId: string;
    name: string;
    type : "cardio" | "strength" | "flexibility" | "balance";
    startTime: string;
    totalCaloriesBurned: number;
    durationMinutes?: number;
    exercises: any[];
}
export interface WorkoutDetailed {
    id : string;
    userId: string;
    name: string;
    type : "cardio" | "strength" | "flexibility" | "balance";
    startTime: string;
    totalCaloriesBurned: number;
    durationMinutes?: number;
    exercises: any[];
    createAt: string;
}
