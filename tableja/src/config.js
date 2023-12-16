const dev = {
    API_ENDPOINT: 'http://127.0.0.1:5000',
};

const prod = {
    API_ENDPOINT: 'http://neringamaja.pythonanywhere.com',
};

const config = process.env.NODE_ENV === 'development' ? dev : prod;

export default config;
