FROM python:3.12.8-bullseye

RUN wget https://dot.net/v1/dotnet-install.sh

RUN chmod +x dotnet-install.sh

RUN ./dotnet-install.sh --channel 6.0

ENV PATH="/root/.dotnet:${PATH}"

RUN dotnet --version

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN mkdir -p analysis

COPY . /analysis

ENV PYTHONPATH=/analysis

EXPOSE 5000

ENV DATABASE_URL="postgresql+psycopg2://mse_owner:CYXP4fDEiH5g@ep-bold-dream-a2fi281z.eu-central-1.aws.neon.tech:5432/mse?sslmode=require&options=endpoint%3Dep-bold-dream-a2fi281z"

#ENTRYPOINT ["tail", "-f", "/dev/null"]
ENTRYPOINT ["python", "-m", "analysis.app"]