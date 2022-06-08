FROM docker.io/fnndsc/mni-conda-base:civet2.1.1-python3.10.4

LABEL org.opencontainers.image.authors="FNNDSC <dev@babyMRI.org>" \
      org.opencontainers.image.title="pl-nii2mnc-u8" \
      org.opencontainers.image.description="A ChRIS ds plugin wrapper for nii2mnc -unsigned -byte"

WORKDIR /usr/local/src/pl-nii2mnc-u8

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN pip install .

CMD ["nii2mnc_wrapper", "--help"]
