FROM ingi/inginious-c-python3
LABEL   org.inginious.grading.name="python3-correcteur"


RUN pip3 install astunparse
RUN mkdir -p /python
COPY correcteur /python/correcteur
ENV PYTHONPATH="/python:${PYTHONPATH}"
