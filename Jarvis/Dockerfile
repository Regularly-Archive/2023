FROM cdrx/pyinstaller-windows

COPY . /src/
COPY ./entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

ENV $PYPI_URL=https://pypi.tuna.tsinghua.edu.cn/
ENV $PYPI_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple 

RUN pip install pip -U
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple


ENTRYPOINT ["entrypoint.sh"]