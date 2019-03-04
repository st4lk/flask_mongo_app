FROM python:3.7.2

RUN mkdir -p /flask_project
RUN useradd -ms /bin/bash appuser
RUN chown -R appuser:appuser /flask_project

RUN mkdir -p /opt/runtime/
ADD scripts/* /opt/runtime/
USER appuser

ENTRYPOINT ["/opt/runtime/entrypoint.sh"]
