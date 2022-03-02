FROM python:3.10-alpine

WORKDIR /usr/src/app

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

RUN \
    # Common resources
    apk add --update --no-cache --virtual build-dependencies \
    file make gcc g++ musl-dev libffi-dev openssl-dev curl gpgme && \
    apk add --update --no-cache --virtual run-dependencies \
    # SQLite (delete section if not needed)
    sqlite \
    # PostgreSQL (delete section if not needed)
    postgresql-dev \
    # MySQL (delete section if not needed)
    mariadb-dev \
    # Neo4J (delete section if not needed)
    geos \
    # SQLServer (delete section if not needed)
    unixodbc-dev unixodbc && \
    curl -L https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.8.1.1-1_amd64.apk -o /tmp/msodbcsql17.apk && \
    curl -L https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.8.1.1-1_amd64.apk -o /tmp/mssql-tools.apk && \
    curl -L https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/msodbcsql17_17.8.1.1-1_amd64.sig -o /tmp/msodbcsql17.sig && \
    curl -L https://download.microsoft.com/download/e/4/e/e4e67866-dffd-428c-aac7-8d28ddafb39b/mssql-tools_17.8.1.1-1_amd64.sig -o /tmp/mssql-tools.sig && \
    curl https://packages.microsoft.com/keys/microsoft.asc | gpg --import - && \
    gpg --verify /tmp/msodbcsql17.sig /tmp/msodbcsql17.apk && \
    gpg --verify /tmp/mssql-tools.sig /tmp/mssql-tools.apk && \
    apk add --update --no-cache --allow-untrusted /tmp/msodbcsql17.apk /tmp/mssql-tools.apk && \
    rm -rf /tmp/*

COPY requirements.txt requirements.txt

RUN \
    pip install --no-cache-dir -r requirements.txt && \
    # Delete packages needed only on build time
    apk del --update --no-cache build-dependencies

COPY . .

RUN \
    touch /usr/src/app/storage/app/database.sqlite

CMD ["python", "./main.py"]
