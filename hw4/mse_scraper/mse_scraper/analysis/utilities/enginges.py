from sqlalchemy import create_engine

def my_engine():
    return create_engine(
        "postgresql+psycopg2://mse_owner:CYXP4fDEiH5g@ep-bold-dream-a2fi281z.eu-central-1.aws.neon.tech:5432/mse"
    )