FROM python:2

RUN mkdir -p /usr/src/hunter
WORKDIR /usr/src/hunter

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

CMD [ "python", "src/FirstApp.py" ]

