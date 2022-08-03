FROM debian

ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY requirements.txt ./

RUN buildDeps='python3 python3-pip nano git bash-completion openssh-server sshpass' && \
apt-get update && apt-get install -y $buildDeps --no-install-recommends --fix-missing && \
pip3 install -r requirements.txt && \
ansible-galaxy collection install cisco.nso && \
ansible-galaxy collection install community.vmware && \
apt-get clean autoclean && \
apt-get autoremove --yes

