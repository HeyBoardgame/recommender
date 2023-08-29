FROM public.ecr.aws/lambda/python:3.11-arm64

COPY requirements.txt ${LAMBDA_TASK_ROOT}

COPY src ${LAMBDA_TASK_ROOT}/src

RUN pip3 install --upgrade -r requirements.txt

RUN pip3 install scikit-surprise==1.1.3

CMD [ "src.main.handler" ]