mkdir -p ~/.streamlit/
echo "[general]
email = \"info@jmbenlloch.net\"
" > ~/.streamlit/credentials.toml
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
