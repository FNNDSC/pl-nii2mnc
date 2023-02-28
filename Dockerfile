FROM docker.io/fnndsc/pl-nii2mnc:base-1

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="pl-nii2mnc" \
      org.opencontainers.image.description="A ChRIS ds plugin wrapper for nii2mnc"

WORKDIR /usr/local/src/pl-nii2mnc

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install .

CMD ["niis2mncs", "--help"]
