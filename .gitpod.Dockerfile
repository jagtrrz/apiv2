FROM gitpod/workspace-full:latest

# Redis
#   redis-server

# PostgreSQL
#    postgresql
#    postgresql-contrib

# Python
#    python3.9
#    python3-pip

RUN sudo apt-get update \
 && sudo add-apt-repository ppa:deadsnakes/ppa \
 && sudo apt-get update \
 && sudo apt-get install -y redis-server postgresql postgresql-contrib python3.9 python3-pip python3-dev \
 && sudo apt-get clean \
 && sudo rm -rf /var/cache/apt/* /var/lib/apt/lists/* /tmp/*

# Setup PostgreSQL server for user gitpod
ENV PATH="$PATH:/usr/lib/postgresql/12/bin"
ENV PGDATA="/home/gitpod/.pg_ctl/data"
RUN mkdir -p ~/.pg_ctl/bin ~/.pg_ctl/data ~/.pg_ctl/sockets \
 && initdb -D ~/.pg_ctl/data/ \
 && printf "#!/bin/bash\npg_ctl -D ~/.pg_ctl/data/ -l ~/.pg_ctl/log -o \"-k ~/.pg_ctl/sockets\" start\n" > ~/.pg_ctl/bin/pg_start \
 && printf "#!/bin/bash\npg_ctl -D ~/.pg_ctl/data/ -l ~/.pg_ctl/log -o \"-k ~/.pg_ctl/sockets\" stop\n" > ~/.pg_ctl/bin/pg_stop \
 && chmod +x ~/.pg_ctl/bin/*
ENV PATH="$PATH:$HOME/.pg_ctl/bin"
ENV PGHOSTADDR="127.0.0.1"
ENV PGDATABASE="postgres"

RUN pyenv update && pyenv install 3.9.1 && pyenv global 3.9.1
RUN pip install pipenv

# This is a bit of a hack. At the moment we have no means of starting background
# tasks from a Dockerfile. This workaround checks, on each bashrc eval, if the
# PostgreSQL server is running, and if not starts it.
RUN printf "\n# Auto-start PostgreSQL server.\n[[ \$(pg_ctl status | grep PID) ]] || pg_start > /dev/null\n" >> ~/.bashrc