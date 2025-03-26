FROM archlinux:latest

LABEL maintainer="mateusz.luczynski02@gmail.com"

RUN pacman -Syu --noconfirm \
  && pacman -S --noconfirm python gcc ffcall base-devel git \
  && pacman -Scc --noconfirm

RUN curl -L -R https://www.lua.org/ftp/lua-5.4.7.tar.gz -o /tmp/lua-5.4.7.tar.gz \
  && cd /tmp \
  && tar zxf lua-5.4.7.tar.gz \
  && cd lua-5.4.7 \
  && make linux test \
  && make install \
  && cd / && rm -rf /tmp/lua-5.4.7 /tmp/lua-5.4.7.tar.gz

RUN git clone https://github.com/mluczynskii/cbind.git /workspace/cbind

WORKDIR /workspace/cbind

CMD [ "bash" ]