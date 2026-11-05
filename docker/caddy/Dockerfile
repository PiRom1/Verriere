# Caddy officiel + module DNS DuckDNS (nécessaire pour obtenir le certificat
# Let's Encrypt sans ouvrir le port 80, déjà pris par giga-serveur).
FROM caddy:2-builder AS builder
RUN xcaddy build --with github.com/caddy-dns/duckdns

FROM caddy:2
COPY --from=builder /usr/bin/caddy /usr/bin/caddy
