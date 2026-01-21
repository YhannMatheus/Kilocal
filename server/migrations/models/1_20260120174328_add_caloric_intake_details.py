from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "caloric_intakes" ADD "name" VARCHAR(100) NOT NULL;
        COMMENT ON COLUMN "caloric_intakes"."name" IS 'Nome da refeição (ex: Almoço, Whey)';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "caloric_intakes" DROP COLUMN "name";"""


MODELS_STATE = (
    "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"
    "5fZy/3+vK4HV"
)
