FROM python:3.8-alpine AS builder

WORKDIR /wheels
COPY dist/* /wheels/
RUN pip wheel napoleon*.whl


FROM python:3.8-alpine

RUN apk --no-cache add \
    git \
    zlib

COPY --from=builder /wheels /wheels
RUN pip install -f /wheels --no-cache-dir napoleon \
    && rm -rf /wheels

CMD ["napoleon"]
