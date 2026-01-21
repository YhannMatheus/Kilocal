from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" UUID NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "name" VARCHAR(255) NOT NULL,
    "hashed_password" VARCHAR(255) NOT NULL,
    "birth_date" DATE NOT NULL,
    "role" VARCHAR(5) NOT NULL DEFAULT 'user',
    "height_cm" DOUBLE PRECISION DEFAULT 0,
    "goal" DOUBLE PRECISION,
    "gender" VARCHAR(6) NOT NULL,
    "activity_level" VARCHAR(17) DEFAULT 'sedentary',
    "activates_at" TIMESTAMPTZ,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "users"."role" IS 'USER: user\nADMIN: admin';
COMMENT ON COLUMN "users"."gender" IS 'MALE: male\nFEMALE: female';
COMMENT ON COLUMN "users"."activity_level" IS 'SEDENTARY: sedentary\nLIGHTLY_ACTIVE: lightly_active\nMODERATELY_ACTIVE: moderately_active\nVERY_ACTIVE: very_active\nEXTRA_ACTIVE: extra_active\nATHLETE: athlete';
CREATE TABLE IF NOT EXISTS "workouts" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "type" VARCHAR(11) NOT NULL,
    "total_calories_burned" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "start_time" TIMESTAMPTZ NOT NULL,
    "end_time" TIMESTAMPTZ,
    "create_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "workouts"."type" IS 'STRENGTH: strength\nCARDIO: cardio\nCROSSFIT: crossfit\nFLEXIBILITY: flexibility\nSPORTS: sports\nBALANCE: balance';
CREATE TABLE IF NOT EXISTS "exercises" (
    "id" UUID NOT NULL PRIMARY KEY,
    "name" VARCHAR(100) NOT NULL,
    "target_muscle" VARCHAR(9) NOT NULL DEFAULT 'chest',
    "instructions" TEXT,
    "is_system_default" BOOL NOT NULL DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "created_by_id" UUID REFERENCES "users" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_exercises_name_d3c5a6" UNIQUE ("name", "created_by_id"),
    CONSTRAINT "uid_exercises_name_a93d70" UNIQUE ("name", "is_system_default")
);
CREATE INDEX IF NOT EXISTS "idx_exercises_name_0b68c8" ON "exercises" ("name");
COMMENT ON COLUMN "exercises"."target_muscle" IS 'BACK: back\nCHEST: chest\nLEGS: legs\nARMS: arms\nSHOULDERS: shoulders\nABDOMEN: abdomen\nCARDIO: cardio';
CREATE TABLE IF NOT EXISTS "sets" (
    "id" UUID NOT NULL PRIMARY KEY,
    "reps" INT,
    "weight" DOUBLE PRECISION,
    "duration" INT,
    "distance" DOUBLE PRECISION,
    "calories_burned" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "exercise_id" UUID NOT NULL REFERENCES "exercises" ("id") ON DELETE CASCADE,
    "workout_id" UUID NOT NULL REFERENCES "workouts" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "body_assessments" (
    "id" UUID NOT NULL PRIMARY KEY,
    "weight_kg" DOUBLE PRECISION NOT NULL,
    "height_cm" DOUBLE PRECISION NOT NULL,
    "waist_cm" DOUBLE PRECISION,
    "hip_cm" DOUBLE PRECISION,
    "chest_cm" DOUBLE PRECISION,
    "neck_cm" DOUBLE PRECISION,
    "arm_cm" DOUBLE PRECISION,
    "thigh_cm" DOUBLE PRECISION,
    "fold_chest" DOUBLE PRECISION,
    "fold_abdominal" DOUBLE PRECISION,
    "fold_thigh" DOUBLE PRECISION,
    "fold_triceps" DOUBLE PRECISION,
    "fold_subscapular" DOUBLE PRECISION,
    "fold_suprailiac" DOUBLE PRECISION,
    "fold_midaxillary" DOUBLE PRECISION,
    "bfp" DOUBLE PRECISION,
    "bmi" DOUBLE PRECISION,
    "bmr" DOUBLE PRECISION,
    "tdee" DOUBLE PRECISION,
    "lean_mass_kg" DOUBLE PRECISION,
    "fat_mass_kg" DOUBLE PRECISION,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "body_assessments"."weight_kg" IS 'Peso total no dia da avaliação';
COMMENT ON COLUMN "body_assessments"."height_cm" IS 'Altura no momento (importante para crianças/jovens)';
CREATE TABLE IF NOT EXISTS "caloric_intakes" (
    "id" UUID NOT NULL PRIMARY KEY,
    "date" DATE NOT NULL,
    "calories_consumed" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "protein_grams" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "carbs_grams" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "fats_grams" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "sessions" (
    "id" UUID NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "expires_at" TIMESTAMPTZ NOT NULL,
    "user_id" UUID NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
    "ecafbk0syKLCpoFy3JT7m83P8fuZANcw=="
)
