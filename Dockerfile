FROM public.ecr.aws/lambda/python:3.10-arm64

COPY requirements.txt ${LAMBDA_TASK_ROOT}

COPY src ${LAMBDA_TASK_ROOT}/src

RUN pip3 install --upgrade -r requirements.txt

CMD [ "src.main.handler" ]