from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ALTER COLUMN "activity_level" SET DEFAULT 'sedentary';
        ALTER TABLE "users" ALTER COLUMN "activity_level" DROP NOT NULL;
        ALTER TABLE "users" ALTER COLUMN "height_cm" DROP NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ALTER COLUMN "activity_level" SET NOT NULL;
        ALTER TABLE "users" ALTER COLUMN "activity_level" DROP DEFAULT;
        ALTER TABLE "users" ALTER COLUMN "height_cm" SET NOT NULL;"""


MODELS_STATE = (
    "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"
    "VYmw=="
)
