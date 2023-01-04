FROM ubuntu:jammy

RUN apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y python3-pip ansible wget git
RUN pip3 install purefusion

RUN mkdir /workdir
WORKDIR /workdir

RUN wget -q --show-progress -O /usr/bin/hmctl https://github.com/PureStorage-OpenConnect/hmctl/releases/latest/download/hmctl-linux-amd64
CMD chmod +x /usr/bin/hmctl

RUN ansible-galaxy collection install purestorage.fusion

RUN mkdir -p /root/.pure
ENV PRIV_KEY_FILE=/workdir/private_key.pem
RUN echo  "{ \"default_profile\": \"main\",\n" \
          " \"profiles\": {\n" \
          "   \"main\": {\n" \
          "     \"env\": \"pure1\",\n" \
          "     \"endpoint\": \"https://api.pure1.purestorage.com/fusion\",\n" \
          "     \"auth\": {\n" \
          "       \"issuer_id\": \"API_CLIENT\",\n" \
          "       \"private_pem_file\": \"/workdir/private_key.pem\"\n" \
          "     }\n" \
          "   }\n" \
          " }\n" \
          "}" > /root/.pure/fusion.json
