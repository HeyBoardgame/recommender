FROM public.ecr.aws/lambda/python:3.10-arm64

COPY requirements.txt ${LAMBDA_TASK_ROOT}

COPY src ${LAMBDA_TASK_ROOT}/src

# scikit-surprise 설치 시 C 컴파일을 위해 컴파일러 설치
RUN yum install gcc -y

RUN pip3 install --upgrade -r requirements.txt

CMD [ "src.main.handler" ]