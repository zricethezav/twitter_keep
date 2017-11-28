TARGET_POSTGRES_PACKAGE="postgresql-9.5-postgis-2.2"
POSTGRES_USER="vagrant"
POSTGRES_PASS="1securePassword"
POSTGRES_DB="twitter"
POSTGRES_REPO_FILE="/etc/apt/sources.list.d/pgdg.list"

log_header() {
    echo -e ""
    echo -e "\033[34m${1}\033[0m"
    echo -e "----------------------"
}

log() {
    echo -e "\033[34m${1}\033[0m"
}

is_package_installed() {
    query_response=$(dpkg-query -f '${db:Status-Abbrev}\t${binary:Package}\t${Version}\n' -W "${1}" | awk '{print $1}')
    return_code=$?

    if  [[ $return_code -eq 1 ]] || [[ "${query_response}" != 'ii' ]]; then
        return 1
    else
        return 0
    fi
}

setup_postgres(){
    log_header "Installing and Configuring PostgreSQL"

    # Check if package exists in local repo
    if [ ! -f "${POSTGRES_REPO_FILE}" ]; then
        log "Installing Tool Dependencies"
        apt-get install --force-yes -q -y wget ca-certificates
        echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > $POSTGRES_REPO_FILE
        wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    else
        log "PgDb Apt-Sources already exist at ${POSTGRES_REPO_FILE}"
    fi

    # Install PostGres if not installed
    is_package_installed "${TARGET_POSTGRES_PACKAGE}"
    return_code=$?
    if  [[ $return_code -eq 1 ]]; then
        apt-get update -q -y
        apt-get install --force-yes -q -y $TARGET_POSTGRES_PACKAGE pgadmin3 postgresql-contrib-9.5
    else
        log "${TARGET_POSTGRES_PACKAGE} already installed."
    fi

    # Create User
    output=$(sudo -u postgres psql -c '\du' -A -F, -t | grep ${POSTGRES_USER})
    return_code=$?
    if [ $return_code -eq 0 ]; then
        log "PostgreSQL User ${POSTGRES_USER} already exists."
    else
        log "Creating PostgreSQL user ${POSTGRES_USER} with password ${POSTGRES_PASS}"
        sudo -u postgres psql -c "create role ${POSTGRES_USER} with superuser createdb login createrole password '${POSTGRES_PASS}'";
    fi

    # Create Twitter DB
    # TODO split out to include multiple dbs (reddit, news sources)
    output=$(sudo -u postgres psql -c '\l' -A -F, -t | grep ${POSTGRES_DB})
    return_code=$?
    if [ $return_code -eq 0 ]; then
        log "Database ${POSTGRES_DB} already exists."
    else
        log "Creating database ${POSTGRES_DB} with owner ${POSTGRES_USER}"
        sudo -u postgres createdb ${POSTGRES_DB} -O ${POSTGRES_USER}
    fi

    # Extensions
    output=$(sudo -u postgres psql -c 'select postgis_version();' -A -F, -t ${POSTGRES_DB})
    return_code=$?
    if [ $return_code -eq 0 ]; then
        log "PostGIS already created in ${POSTGRES_DB}"
    else
        log "Enabling PostGIS on ${POSTGRES_DB}"
        sudo -u postgres psql -c 'create extension postgis; select postgis_version();' ${POSTGRES_DB}
    fi

    # md5 needs to trust local hosting
    sudo sed -i -e s/md5/trust/g /etc/postgresql/9.5/main/pg_hba.conf

    # restart
    sudo /etc/init.d/postgresql restart

}

create_twitter_tables() {
    # good info on building relationships
    # http://blog.bguiz.com/2017/postgres-many2many-sql-non-relational/
    log "Creating Twitter Tables"

    # tweet table
    sudo -u postgres -H -- psql -d twitter -c "DROP TABLE tweets;"
    sudo -u postgres -H -- psql -d twitter -c "DROP TABLE users;"
    sudo -u postgres -H -- psql -d twitter -c "DROP TABLE tweets_users;"

    sudo -u postgres -H -- psql -d twitter -c "CREATE TABLE tweets(
        tweet_id bigint PRIMARY KEY,
        tweet_text varchar(230) NOT NULL,
        created_at timestamp NOT NULL,
        geo_lat decimal(10,5) DEFAULT NULL,
        geo_long decimal(10,5) DEFAULT NULL,
        user_id bigint NOT NULL,
        screen_name char(20) NOT NULL,
        name varchar(20) DEFAULT NULL,
        profile_image_url varchar(200) DEFAULT NULL,
        is_rt smallint NOT NULL);"
    sudo -u postgres -H -- psql -d twitter -c "GRANT ALL PRIVILEGES ON TABLE tweets TO $POSTGRES_USER;"

    # user table
    sudo -u postgres -H -- psql -d twitter -c "CREATE TABLE users(
        user_id bigint PRIMARY KEY,
        screen_name char(20) NOT NULL,
        name varchar(20) DEFAULT NULL,
        profile_image_url varchar(200) DEFAULT NULL,
        location varchar(30) DEFAULT NULL,
        url varchar(200) DEFAULT NULL,
        description varchar(200) DEFAULT NULL,
        created_at timestamp NOT NULL,
        followers_count bigint DEFAULT NULL,
        friends_count bigint DEFAULT NULL,
        statuses_count bigint DEFAULT NULL,
        time_zone varchar(40) DEFAULT NULL,
        last_update timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
    );"
    sudo -u postgres -H -- psql -d twitter -c "GRANT ALL PRIVILEGES ON TABLE users TO $POSTGRES_USER;"

    # tweet_user table
    sudo -u postgres -H -- psql -d twitter -c "CREATE TABLE IF NOT EXISTS tweets_users(
        user_id bigint REFERENCES users,
        tweet_id bigint REFERENCES tweets,
        constraint id PRIMARY KEY (user_id, tweet_id)
    );"
    sudo -u postgres -H -- psql -d twitter -c "GRANT ALL PRIVILEGES ON TABLE tweets_users TO $POSTGRES_USER;"
}

setup_postgres


# create tables, first to process is twitter
create_twitter_tables
