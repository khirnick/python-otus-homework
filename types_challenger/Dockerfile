FROM python:3.11-slim

WORKDIR /types_challanger
COPY . .

RUN pip install mypy pyright

CMD ["./run_lint.sh"]
