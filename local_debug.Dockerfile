# Chrome Web Brouser for Selenium Automate Development
FROM public.ecr.aws/lambda/python:3.10 as build
RUN yum install -y unzip && \
    curl -Lo "/tmp/chromedriver-linux64.zip" "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chromedriver-linux64.zip" && \
    curl -Lo "/tmp/chrome-linux64.zip" "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chrome-linux64.zip" && \
    unzip /tmp/chromedriver-linux64.zip -d /opt/ && \
    unzip /tmp/chrome-linux64.zip -d /opt/

FROM public.ecr.aws/lambda/python:3.10
RUN yum install -y atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel nss mesa-libgbm
COPY --from=build /opt/chrome-linux64 /opt/chrome
COPY --from=build /opt/chromedriver-linux64 /opt/

# Install poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python \
    && cd /usr/local/bin \
    && ln -s /opt/poetry/bin/poetry \
    && poetry config virtualenvs.create false

COPY src/ ${LAMBDA_TASK_ROOT}/
COPY pyproject.toml poetry.lock ${LAMBDA_TASK_ROOT}/
# Install python packages
RUN poetry install --no-root
