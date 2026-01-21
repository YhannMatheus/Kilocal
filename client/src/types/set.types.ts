export interface SetCreate {
    exerciseId: string;
    reps?: number;
    weight?: number;
    durationSeconds?: number;
}

export interface SetUpdate {
    reps?: number;
    weight?: number;
    durationSeconds?: number;
}

export interface SetRead {
    id: string;
    exerciseId: string;
    reps?: number;
    weight?: number;
    durationSeconds?: number;
    createdAt: string;
}