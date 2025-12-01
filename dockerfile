FROM ubuntu:resolute-20251101

ENV LANG=C.UTF-8
ENV TZ=Asia/Ho_Chi_Minh

USER 0

RUN apt-get update && apt-get install -y curl wget nano python3 python3-pip && apt-get clean

RUN pip3 install --break-system-packages --ignore-installed urllib3 poetry

COPY . /workspace
RUN chmod +x -R /workspace/bin

WORKDIR /workspace
ENTRYPOINT ["bash", "-lc"]
CMD ["bash /workspace/bin/entrypoint"]